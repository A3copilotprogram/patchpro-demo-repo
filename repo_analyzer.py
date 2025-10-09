"""
Repository Analysis Module for PatchPro Demo
Handles full repository cloning, analysis, and reporting with AI-powered fixes
"""
import os
import json
import subprocess
import tempfile
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import requests
from urllib.parse import urlparse
import time

# Import PatchPro integration for AI fixes
try:
    from patchpro_integration import PatchProIntegration
    PATCHPRO_AVAILABLE = True
except ImportError:
    PATCHPRO_AVAILABLE = False
    print("[INFO] PatchPro integration not available, fixes will be skipped")

class RepositoryAnalyzer:
    """Analyzes entire repositories for code quality issues"""
    
    def __init__(self, max_files: int = 50, max_file_size: int = 100000):
        """
        Initialize repository analyzer
        
        Args:
            max_files: Maximum number of Python files to analyze
            max_file_size: Maximum file size in bytes (100KB default)
        """
        self.max_files = max_files
        self.max_file_size = max_file_size
        self.supported_extensions = {'.py'}
        self.excluded_dirs = {
            '__pycache__', '.git', '.pytest_cache', '.tox', 'venv', 
            'env', '.env', 'node_modules', '.vscode', '.idea',
            'build', 'dist', '*.egg-info', '.mypy_cache', '.coverage',
            'htmlcov', '.pytest', 'site-packages'
        }
        self.excluded_files = {
            'setup.py', 'conftest.py'  # Often have different standards
        }
    
    def analyze_repository(self, repo_url: str, branch: str = "main") -> Dict[str, Any]:
        """
        Analyze a complete repository
        
        Args:
            repo_url: GitHub repository URL or zip download URL
            branch: Git branch to analyze (default: main)
            
        Returns:
            Dict containing comprehensive analysis results
        """
        start_time = time.time()
        
        try:
            # Create temporary directory for analysis
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Clone or download repository
                repo_path = self._download_repository(repo_url, temp_path, branch)
                if not repo_path:
                    return {"error": "Failed to download repository"}
                
                # Discover Python files
                python_files = self._discover_python_files(repo_path)
                
                if not python_files:
                    return {
                        "error": "No Python files found in repository",
                        "repo_url": repo_url,
                        "files_checked": 0
                    }
                
                # Limit files for performance
                if len(python_files) > self.max_files:
                    python_files = python_files[:self.max_files]
                    truncated = True
                else:
                    truncated = False
                
                # Analyze each file
                results = self._analyze_files(python_files, repo_path)
                
                # Generate summary
                summary = self._generate_summary(results, repo_url, branch)
                summary['analysis_time'] = round(time.time() - start_time, 2)
                summary['files_truncated'] = truncated
                summary['max_files_limit'] = self.max_files
                
                return summary
                
        except Exception as e:
            return {
                "error": f"Repository analysis failed: {str(e)}",
                "repo_url": repo_url,
                "analysis_time": round(time.time() - start_time, 2)
            }
    
    def _download_repository(self, repo_url: str, temp_path: Path, branch: str) -> Optional[Path]:
        """Download repository to temporary directory"""
        try:
            # Parse GitHub URL
            if "github.com" in repo_url:
                # Convert to download URL
                repo_url = repo_url.rstrip('/')
                if repo_url.endswith('.git'):
                    repo_url = repo_url[:-4]
                
                # Try zip download first (faster than git clone)
                zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
                
                response = requests.get(zip_url, timeout=30, stream=True)
                
                if response.status_code == 200:
                    # Download and extract zip
                    zip_path = temp_path / "repo.zip"
                    with open(zip_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Extract zip
                    extract_path = temp_path / "extracted"
                    extract_path.mkdir()
                    
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_path)
                    
                    # Find the extracted directory (usually has repo name + branch)
                    extracted_dirs = list(extract_path.iterdir())
                    if extracted_dirs:
                        return extracted_dirs[0]
                    
                else:
                    # Fallback to git clone
                    return self._git_clone(repo_url, temp_path, branch)
            
            else:
                return {"error": "Only GitHub repositories are supported currently"}
                
        except Exception as e:
            print(f"Download error: {str(e)}")
            return None
    
    def _git_clone(self, repo_url: str, temp_path: Path, branch: str) -> Optional[Path]:
        """Clone repository using git"""
        try:
            clone_path = temp_path / "repo"
            
            # Clone with specific branch and depth 1 for speed
            result = subprocess.run([
                'git', 'clone', '--depth', '1', '--branch', branch, 
                repo_url, str(clone_path)
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return clone_path
            else:
                print(f"Git clone failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Git clone error: {str(e)}")
            return None
    
    def _discover_python_files(self, repo_path: Path) -> List[Path]:
        """Discover all Python files in repository"""
        python_files = []
        
        def should_skip_dir(dir_path: Path) -> bool:
            """Check if directory should be skipped"""
            dir_name = dir_path.name
            return (
                dir_name.startswith('.') or
                dir_name in self.excluded_dirs or
                any(pattern in dir_name for pattern in ['__pycache__', '.egg-info'])
            )
        
        def should_skip_file(file_path: Path) -> bool:
            """Check if file should be skipped"""
            return (
                file_path.name in self.excluded_files or
                file_path.name.startswith('.') or
                file_path.stat().st_size > self.max_file_size or
                file_path.stat().st_size == 0  # Skip empty files
            )
        
        def scan_directory(path: Path):
            """Recursively scan directory for Python files"""
            try:
                for item in path.iterdir():
                    if item.is_file():
                        if (item.suffix in self.supported_extensions and 
                            not should_skip_file(item)):
                            python_files.append(item)
                    elif item.is_dir() and not should_skip_dir(item):
                        scan_directory(item)
            except (PermissionError, OSError):
                pass  # Skip inaccessible directories
        
        scan_directory(repo_path)
        
        # Sort by file size (smaller files first for faster processing)
        python_files.sort(key=lambda f: f.stat().st_size)
        return python_files
    
    def _analyze_files(self, files: List[Path], repo_path: Path) -> Dict[str, Any]:
        """Analyze list of Python files"""
        results = {
            'files': {},
            'total_files': len(files),
            'total_issues': 0,
            'categories': {'security': 0, 'quality': 0, 'style': 0},
            'analysis_errors': [],
            'file_stats': {
                'with_issues': 0,
                'without_issues': 0,
                'analysis_failed': 0
            }
        }
        
        print(f"[INFO] Analyzing {len(files)} Python files...")
        
        for i, file_path in enumerate(files, 1):
            try:
                # Get relative path for display
                rel_path = file_path.relative_to(repo_path)
                
                if i % 10 == 0 or i == len(files):
                    print(f"[INFO] Progress: {i}/{len(files)} files analyzed")
                
                # Analyze single file
                file_result = self._analyze_single_file(file_path)
                
                if 'error' not in file_result:
                    results['files'][str(rel_path)] = file_result
                    results['total_issues'] += file_result['issue_count']
                    
                    # Update statistics
                    if file_result['issue_count'] > 0:
                        results['file_stats']['with_issues'] += 1
                    else:
                        results['file_stats']['without_issues'] += 1
                    
                    # Update categories
                    for category, count in file_result['categories'].items():
                        results['categories'][category] += count
                else:
                    results['analysis_errors'].append({
                        'file': str(rel_path),
                        'error': file_result['error']
                    })
                    results['file_stats']['analysis_failed'] += 1
                    
            except Exception as e:
                results['analysis_errors'].append({
                    'file': str(file_path.name),
                    'error': str(e)
                })
                results['file_stats']['analysis_failed'] += 1
        
        print(f"[INFO] Analysis complete: {results['total_issues']} total issues found")
        return results
    
    def _analyze_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file"""
        try:
            # Run Ruff on the file
            result = subprocess.run([
                'python3', '-m', 'ruff', 'check', 
                '--output-format=json', str(file_path)
            ], capture_output=True, text=True, timeout=10)
            
            # Parse Ruff output
            issues = []
            if result.stdout:
                try:
                    raw_issues = json.loads(result.stdout)
                    issues = self._format_issues(raw_issues)
                except json.JSONDecodeError:
                    pass
            
            # Categorize issues
            categories = {'security': 0, 'quality': 0, 'style': 0}
            for issue in issues:
                code = issue.get('code', '')
                if code.startswith('S'):
                    categories['security'] += 1
                elif code.startswith(('F', 'E')):
                    categories['quality'] += 1
                else:
                    categories['style'] += 1
            
            # Read file content for context
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines_count = len(content.splitlines())
                size_bytes = len(content.encode('utf-8'))
            except:
                lines_count = 0
                size_bytes = 0
            
            return {
                'issue_count': len(issues),
                'issues': issues[:20],  # Limit issues per file
                'categories': categories,
                'lines_count': lines_count,
                'size_bytes': size_bytes,
                'truncated_issues': len(issues) > 20
            }
            
        except subprocess.TimeoutExpired:
            return {'error': 'Analysis timeout'}
        except Exception as e:
            return {'error': str(e)}
    
    def _format_issues(self, raw_issues: List[Dict]) -> List[Dict]:
        """Format Ruff issues to consistent format"""
        formatted = []
        for issue in raw_issues:
            formatted.append({
                'code': issue.get('code', 'UNKNOWN'),
                'message': issue.get('message', 'No message'),
                'line': issue.get('location', {}).get('row', 0),
                'column': issue.get('location', {}).get('column', 0),
                'severity': 'error' if issue.get('code', '').startswith('F') else 'warning'
            })
        return formatted
    
    def _generate_summary(self, results: Dict[str, Any], repo_url: str, branch: str) -> Dict[str, Any]:
        """Generate comprehensive analysis summary"""
        files_with_issues = {
            path: data for path, data in results['files'].items() 
            if data['issue_count'] > 0
        }
        
        # Find top problematic files
        top_files = sorted(
            files_with_issues.items(),
            key=lambda x: x[1]['issue_count'],
            reverse=True
        )[:10]
        
        # Calculate statistics
        total_lines = sum(data['lines_count'] for data in results['files'].values())
        total_size = sum(data['size_bytes'] for data in results['files'].values())
        
        # Calculate quality metrics
        issue_density = round(results['total_issues'] / max(total_lines, 1) * 1000, 2)
        
        # Determine overall quality grade
        if issue_density == 0:
            quality_grade = "A+"
        elif issue_density < 5:
            quality_grade = "A"
        elif issue_density < 10:
            quality_grade = "B"
        elif issue_density < 20:
            quality_grade = "C"
        else:
            quality_grade = "D"
        
        # File type analysis
        file_types = {}
        for path, data in results['files'].items():
            if '/' in path:
                directory = path.split('/')[0]
            else:
                directory = 'root'
            
            if directory not in file_types:
                file_types[directory] = {'files': 0, 'issues': 0}
            file_types[directory]['files'] += 1
            file_types[directory]['issues'] += data['issue_count']
        
        return {
            'success': True,
            'repository': {
                'url': repo_url,
                'branch': branch,
                'total_files': results['total_files'],
                'files_analyzed': len(results['files']),
                'total_lines': total_lines,
                'total_size_bytes': total_size,
                'size_mb': round(total_size / (1024 * 1024), 2)
            },
            'analysis': {
                'total_issues': results['total_issues'],
                'files_with_issues': len(files_with_issues),
                'categories': results['categories'],
                'issue_density': issue_density,
                'quality_grade': quality_grade,
                'file_stats': results['file_stats']
            },
            'top_problematic_files': [
                {
                    'file': path,
                    'issues': data['issue_count'],
                    'categories': data['categories'],
                    'lines': data['lines_count'],
                    'issue_density': round(data['issue_count'] / max(data['lines_count'], 1) * 100, 1)
                }
                for path, data in top_files
            ],
            'directory_analysis': dict(sorted(
                file_types.items(), 
                key=lambda x: x[1]['issues'], 
                reverse=True
            )[:5]),  # Top 5 directories by issue count
            'file_details': results['files'],
            'errors': results['analysis_errors']
        }

    def _generate_fixes_for_file(self, file_path: Path, issues: List[Dict]) -> Dict[str, Any]:
        """Generate AI-powered fixes for a file with issues"""
        if not PATCHPRO_AVAILABLE or not issues:
            return {"fixes_available": False, "reason": "No PatchPro integration or no issues"}
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Use PatchPro integration to generate fixes
            integration = PatchProIntegration()
            result = integration.analyze_and_fix_sync(code, issues)
            
            if result.get('agent_core_used') and result.get('fixed_code'):
                return {
                    "fixes_available": True,
                    "original_code": code,
                    "fixed_code": result['fixed_code'],
                    "fix_summary": result.get('analysis_summary', 'Fixed using AgentCore'),
                    "agent_core_used": True,
                    "issues_addressed": len(issues)
                }
            else:
                return {"fixes_available": False, "reason": "Fix generation failed"}
                
        except Exception as e:
            return {"fixes_available": False, "reason": f"Fix error: {str(e)}"}

    def analyze_repository_with_fixes(self, repo_url: str, branch: str = "main", 
                                    generate_fixes: bool = False) -> Dict[str, Any]:
        """
        Enhanced repository analysis with optional AI-powered fixes
        
        Args:
            repo_url: GitHub repository URL
            branch: Git branch to analyze
            generate_fixes: Whether to generate AI fixes for problematic files
            
        Returns:
            Dict containing analysis results with optional fixes
        """
        # Run standard analysis first
        analysis_result = self.analyze_repository(repo_url, branch)
        
        if generate_fixes and 'error' not in analysis_result and PATCHPRO_AVAILABLE:
            print("[INFO] Generating AI fixes for problematic files...")
            
            # Get top problematic files for fixing
            top_files = analysis_result.get('top_problematic_files', [])[:5]  # Fix top 5 files
            
            fixes_generated = []
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Re-download repository for fixing
                repo_path = self._download_repository(repo_url, temp_path, branch)
                if repo_path:
                    for file_info in top_files:
                        file_path = repo_path / file_info['file']
                        if file_path.exists():
                            # Get issues for this file
                            file_details = analysis_result['file_details'].get(file_info['file'], {})
                            issues = file_details.get('issues', [])
                            
                            if issues:
                                fix_result = self._generate_fixes_for_file(file_path, issues)
                                fix_result['file'] = file_info['file']
                                fix_result['original_issues'] = len(issues)
                                fixes_generated.append(fix_result)
            
            # Add fixes to analysis result
            analysis_result['fixes_generated'] = fixes_generated
            analysis_result['total_files_fixed'] = len([f for f in fixes_generated if f.get('fixes_available')])
            analysis_result['agentcore_fixes_available'] = PATCHPRO_AVAILABLE
            
        return analysis_result

    def get_repository_info(self, repo_url: str) -> Dict[str, Any]:
        """Get basic repository information without full analysis"""
        try:
            if "github.com" in repo_url:
                # Extract owner/repo from URL
                parts = repo_url.rstrip('/').split('/')
                if len(parts) >= 2:
                    owner = parts[-2]
                    repo = parts[-1]
                    if repo.endswith('.git'):
                        repo = repo[:-4]
                    
                    # GitHub API call for repo info
                    api_url = f"https://api.github.com/repos/{owner}/{repo}"
                    response = requests.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            'name': data.get('name'),
                            'description': data.get('description'),
                            'language': data.get('language'),
                            'stars': data.get('stargazers_count'),
                            'forks': data.get('forks_count'),
                            'size': data.get('size'),  # KB
                            'default_branch': data.get('default_branch'),
                            'last_updated': data.get('updated_at')
                        }
            
            return {'error': 'Could not fetch repository information'}
            
        except Exception as e:
            return {'error': f'Failed to get repo info: {str(e)}'}