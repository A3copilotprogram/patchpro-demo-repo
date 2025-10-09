"""
PatchPro Bot Integration Module
Wrapper for integrating PatchPro Bot's agentic system into the demo app
"""
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path
import tempfile
import logging

try:
    from patchpro_bot import AgentCore, AgentConfig
    from patchpro_bot.agentic_patch_generator_v2 import AgenticPatchGeneratorV2
    from patchpro_bot.models import AnalysisFinding, CodeLocation
    PATCHPRO_AVAILABLE = True
except ImportError:
    PATCHPRO_AVAILABLE = False
    logging.warning("PatchPro Bot not available - enabling mock demonstration mode")

# Import mock implementation for demonstration
try:
    from mock_patchpro_bot import MockAgentCore, create_mock_agentcore, get_mock_integration_status
    MOCK_AVAILABLE = True
except ImportError:
    MOCK_AVAILABLE = False
    logging.error("Mock PatchPro Bot also not available")


class PatchProIntegration:
    """Wrapper for PatchPro Bot agentic system integration"""
    
    def __init__(self, api_key: str):
        """
        Initialize PatchPro Bot integration
        
        Args:
            api_key: OpenAI API key for LLM access
        """
        self.api_key = api_key
        self.using_mock = False
        
        if PATCHPRO_AVAILABLE:
            # Use real PatchPro Bot
            self.config = AgentConfig(
                openai_api_key=api_key,
                llm_model="gpt-4o-mini",
                enable_agentic_mode=True,
                agentic_max_retries=3,
                agentic_enable_planning=True,
                max_tokens=4096,
                temperature=0.1
            )
            logging.info("PatchPro Bot integration initialized with agentic mode enabled")
            
        elif MOCK_AVAILABLE:
            # Use mock implementation for demonstration
            self.mock_agentcore = create_mock_agentcore(api_key)
            self.using_mock = True
            logging.info("🎭 PatchPro Bot Mock Mode: Demonstrating agentic capabilities")
            
        else:
            raise ImportError(
                "Neither PatchPro Bot nor mock implementation available. "
                "This is needed to demonstrate the agentic system."
            )
    
    async def analyze_and_fix_async(
        self,
        code: str,
        issues: List[Dict[str, Any]],
        filename: str = "code.py"
    ) -> Dict[str, Any]:
        """
        Analyze code and generate fixes using PatchPro Bot's agentic system
        
        Args:
            code: Source code to analyze
            issues: List of Ruff issues to fix
            filename: Name of the file being analyzed
            
        Returns:
            Dict containing fixed code, analysis, and agent metadata
        """
        if self.using_mock:
            # Use mock AgentCore for demonstration
            logging.info(f"🎭 Using Mock AgentCore to demonstrate agentic analysis of {filename}")
            return self.mock_agentcore.analyze_and_fix(code, issues, filename)
        
        # Use real PatchPro Bot
        # Convert issues to PatchPro findings
        findings = self._convert_to_findings(code, issues, filename)
        
        if not findings:
            return {
                'success': False,
                'error': 'No valid findings to process',
                'agent_used': True
            }
        
        # Create temporary directory for analysis
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Write code to temporary file
            code_file = tmpdir_path / filename
            code_file.write_text(code)
            
            # Update config with temp directory
            self.config.base_dir = str(tmpdir_path)
            
            try:
                # Create agentic patch generator
                generator = AgenticPatchGeneratorV2(agent_config=self.config)
                
                logging.info(f"Starting PatchPro agent analysis for {len(findings)} findings")
                
                # Generate patches with agentic system
                result = await generator.achieve_goal(
                    goal="fix_all_findings",
                    findings=findings,
                    source_code=code
                )
                
                logging.info(f"PatchPro agent completed: {result.get('success', False)}")
                
                return self._format_result(result, code)
                
            except Exception as e:
                logging.error(f"PatchPro agent error: {str(e)}")
                return {
                    'success': False,
                    'error': f"Agent analysis failed: {str(e)}",
                    'agent_used': True
                }
    
    def analyze_and_fix_sync(
        self,
        code: str,
        issues: List[Dict[str, Any]],
        filename: str = "code.py"
    ) -> Dict[str, Any]:
        """
        Synchronous wrapper for analyze_and_fix_async
        
        Args:
            code: Source code to analyze
            issues: List of Ruff issues to fix
            filename: Name of the file being analyzed
            
        Returns:
            Dict containing fixed code, analysis, and agent metadata
        """
        if self.using_mock:
            # Use mock AgentCore for demonstration
            logging.info(f"🎭 Using Mock AgentCore (sync) to demonstrate agentic analysis of {filename}")
            return self.mock_agentcore.analyze_and_fix(code, issues, filename)
        
        # Use real PatchPro Bot with async wrapper
        try:
            return asyncio.run(self.analyze_and_fix_async(code, issues, filename))
        except Exception as e:
            logging.error(f"Sync analysis failed: {str(e)}")
            return {
                'success': False,
                'error': f"Synchronous analysis failed: {str(e)}",
                'agent_used': True
            }
    
    def _convert_to_findings(
        self,
        code: str,
        issues: List[Dict[str, Any]],
        filename: str
    ) -> List[AnalysisFinding]:
        """
        Convert demo issues to PatchPro AnalysisFinding objects
        
        Args:
            code: Source code
            issues: List of Ruff issues
            filename: Name of the file
            
        Returns:
            List of AnalysisFinding objects
        """
        findings = []
        
        for issue in issues:
            try:
                # Determine severity
                code_prefix = issue['code'].split('-')[0] if '-' in issue['code'] else issue['code'][0]
                severity = 'error' if code_prefix in ['F', 'E'] else 'warning'
                
                # Create finding
                finding = AnalysisFinding(
                    rule_id=issue['code'],
                    message=issue['message'],
                    severity=severity,
                    file_path=filename,
                    location=CodeLocation(
                        start_line=issue.get('line', 1),
                        start_column=issue.get('column', 0),
                        end_line=issue.get('end_line', issue.get('line', 1)),
                        end_column=issue.get('end_column', issue.get('column', 0))
                    ),
                    tool='ruff',
                    category='quality'
                )
                findings.append(finding)
                
            except Exception as e:
                logging.error(f"Failed to convert issue to finding: {issue}, error: {str(e)}")
                continue
        
        logging.info(f"Converted {len(findings)} issues to PatchPro findings")
        return findings
    
    def _format_result(self, result: Dict[str, Any], original_code: str) -> Dict[str, Any]:
        """
        Format PatchPro result for demo app response
        
        Args:
            result: Result from PatchPro agent
            original_code: Original source code
            
        Returns:
            Formatted result dict
        """
        if not result.get('success'):
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'agent_used': True,
                'agent_metadata': {
                    'attempts': result.get('attempts', 0),
                    'success_rate': 0.0
                }
            }
        
        # Build analysis text
        analysis_parts = []
        analysis_parts.append("🤖 **PatchPro Agent Analysis**\n")
        
        # Agent metadata
        attempts = result.get('attempts', 1)
        success_rate = result.get('success_rate', 1.0)
        analysis_parts.append(f"- **Attempts:** {attempts}")
        analysis_parts.append(f"- **Success Rate:** {success_rate:.1%}")
        analysis_parts.append(f"- **Strategy:** {result.get('strategy', 'unified_diff')}\n")
        
        # Patches info
        patches = result.get('patches', [])
        if patches:
            analysis_parts.append(f"**Generated {len(patches)} patch(es):**\n")
            for i, patch in enumerate(patches, 1):
                analysis_parts.append(f"{i}. {patch.get('description', 'Code fix')}")
        
        # Detailed analysis
        if result.get('analysis'):
            analysis_parts.append(f"\n**Changes Made:**\n{result['analysis']}")
        
        return {
            'success': True,
            'fixed_code': result.get('fixed_code', original_code),
            'analysis': '\n'.join(analysis_parts),
            'agent_used': True,
            'agent_metadata': {
                'attempts': attempts,
                'success_rate': success_rate,
                'strategy': result.get('strategy', 'unified_diff'),
                'patches_count': len(patches),
                'agent_version': 'v2'
            }
        }




def is_patchpro_available() -> bool:
    """Check if PatchPro Bot is available (real or mock)"""
    return PATCHPRO_AVAILABLE or MOCK_AVAILABLE


def get_integration_status() -> Dict[str, Any]:
    """Get PatchPro Bot integration status"""
    if PATCHPRO_AVAILABLE:
        return {
            'available': True,
            'version': 'v2',
            'mode': 'production',
            'features': {
                'agentic_mode': True,
                'self_correction': True,
                'retry_logic': True,
                'patch_validation': True
            }
        }
    elif MOCK_AVAILABLE:
        return get_mock_integration_status()
    else:
        return {
            'available': False,
            'version': None,
            'mode': 'unavailable',
            'features': {}
        }
