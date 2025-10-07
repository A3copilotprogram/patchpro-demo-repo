"""
PatchPro Demo - Interactive Code Analysis Web Interface
A Flask application with live code analysis capabilities for Render.com deployment
"""
from flask import Flask, jsonify, render_template_string, request
import os
import sys
import subprocess
import json
import tempfile
from pathlib import Path

app = Flask(__name__)

# Sample problematic code snippets for testing
SAMPLE_CODES = {
    "security": '''
import os

def login(username, password):
    # Security issue: Hardcoded credentials
    admin_password = "admin123"
    api_key = "sk-1234567890abcdef"
    
    if password == admin_password:
        return True
    return False
''',
    "quality": '''
import os, sys  # Multiple imports on one line
import json

def process_data(data):
    result = data * 2  # Unused variable
    unused_var = "not used"
    return data * 2
''',
    "style": '''
def bad_function(a,b,c):
    name = "world"
    message = "Hello {}".format(name)  # Should use f-string
    if a>b:  # Missing spaces
        return c
    return None
'''
}

app = Flask(__name__)

# HTML template for the home page with interactive code analysis
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PatchPro Live Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 { 
            color: #333; 
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .badge { 
            display: inline-block;
            padding: 5px 12px;
            background: #4CAF50;
            color: white;
            border-radius: 20px;
            margin: 5px;
            font-size: 12px;
        }
        .section {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .interactive-section {
            background: #fff3cd;
            border-left-color: #ffc107;
        }
        textarea {
            width: 100%;
            min-height: 200px;
            font-family: 'Courier New', monospace;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            margin: 10px 0;
            box-sizing: border-box;
        }
        .btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-sample {
            background: #28a745;
        }
        .btn-sample:hover {
            background: #218838;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border: 2px solid #667eea;
            display: none;
        }
        .result.show {
            display: block;
        }
        .issue {
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            background: #f8d7da;
        }
        .issue.warning {
            border-left-color: #ffc107;
            background: #fff3cd;
        }
        .issue.info {
            border-left-color: #17a2b8;
            background: #d1ecf1;
        }
        code {
            background: #f4f4f4;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }
        .endpoint {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .method {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 12px;
            margin-right: 10px;
        }
        .get { background: #61affe; color: white; }
        .post { background: #49cc90; color: white; }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 PatchPro Live Demo</h1>
        <p class="subtitle">Interactive Code Analysis & Quality Checking</p>
        <div class="badge">Status: Running</div>
        <div class="badge">Python {{ python_version }}</div>
        <div class="badge">Ruff Enabled</div>
        
        <div class="section interactive-section">
            <h2>🚀 Try It Live!</h2>
            <p>Paste your Python code below or load a sample to see PatchPro in action. The analyzer will check for security issues, code quality problems, and style violations.</p>
            
            <div style="margin: 15px 0;">
                <button class="btn btn-sample" onclick="loadSample('security')">Load Security Example</button>
                <button class="btn btn-sample" onclick="loadSample('quality')">Load Quality Example</button>
                <button class="btn btn-sample" onclick="loadSample('style')">Load Style Example</button>
            </div>
            
            <textarea id="codeInput" placeholder="# Paste your Python code here...
# Example:
import os

password = 'hardcoded123'  # This will be flagged!

def my_function():
    unused_var = 'test'
    print('Hello')
"></textarea>
            
            <button class="btn" onclick="analyzeCode()">🔍 Analyze Code</button>
            <button class="btn" onclick="clearResults()">Clear</button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyzing your code...</p>
            </div>
            
            <div class="result" id="result"></div>
        </div>

        <div class="section">
            <h3>📡 API Endpoints</h3>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/</code>
                <p>Interactive web interface (this page)</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/health</code>
                <p>Health check endpoint - returns service status</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/info</code>
                <p>Project information and capabilities</p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/analyze</code>
                <p>Analyze Python code - send JSON with <code>{"code": "your code here"}</code></p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/samples</code>
                <p>Get sample code with common issues</p>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <code>/api/demo-files</code>
                <p>Analyze existing demo files in the repository</p>
            </div>
        </div>

        <div class="section">
            <h3>🔬 What Gets Analyzed?</h3>
            <ul>
                <li>🔒 <strong>Security Issues</strong>: Hardcoded passwords, API keys, SQL injection risks</li>
                <li>📊 <strong>Code Quality</strong>: Unused variables, imports, dead code</li>
                <li>✨ <strong>Style Violations</strong>: PEP 8 compliance, formatting issues</li>
                <li>⚡ <strong>Performance</strong>: Inefficient patterns, optimization opportunities</li>
            </ul>
        </div>

        <div class="section">
            <h3>📖 Repository</h3>
            <p>View source code: <a href="https://github.com/A3copilotprogram/patchpro-demo-repo" target="_blank">GitHub</a></p>
            <p>Powered by: <strong>Ruff</strong> (Python linter) | <strong>Flask</strong> (Web framework)</p>
        </div>
    </div>

    <script>
        const samples = {{ samples | tojson }};
        
        function loadSample(type) {
            document.getElementById('codeInput').value = samples[type];
            clearResults();
        }
        
        function clearResults() {
            document.getElementById('result').classList.remove('show');
            document.getElementById('result').innerHTML = '';
        }
        
        async function analyzeCode() {
            const code = document.getElementById('codeInput').value;
            if (!code.trim()) {
                alert('Please enter some code to analyze!');
                return;
            }
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: code })
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                document.getElementById('result').innerHTML = 
                    '<div class="issue"><strong>Error:</strong> ' + error.message + '</div>';
                document.getElementById('result').classList.add('show');
            } finally {
                document.getElementById('loading').classList.remove('show');
            }
        }
        
        function displayResults(data) {
            const resultDiv = document.getElementById('result');
            
            if (data.error) {
                resultDiv.innerHTML = '<div class="issue"><strong>Error:</strong> ' + data.error + '</div>';
                resultDiv.classList.add('show');
                return;
            }
            
            let html = '<h3>📊 Analysis Results</h3>';
            html += '<p><strong>Total Issues Found:</strong> ' + data.total_issues + '</p>';
            
            if (data.total_issues === 0) {
                html += '<div class="issue info"><strong>✅ Great job!</strong> No issues found in your code!</div>';
            } else {
                html += '<div style="margin: 20px 0;">';
                data.issues.forEach(issue => {
                    const severity = issue.code.startsWith('F') ? 'issue' : 
                                   issue.code.startsWith('E') ? 'warning' : 'info';
                    html += `
                        <div class="issue ${severity}">
                            <strong>${issue.code}</strong>: ${issue.message}<br>
                            <small>Line ${issue.line}, Column ${issue.column}</small>
                        </div>
                    `;
                });
                html += '</div>';
                
                html += '<h4>💡 Issue Categories:</h4><ul>';
                if (data.categories.security > 0) html += '<li>🔒 Security Issues: ' + data.categories.security + '</li>';
                if (data.categories.quality > 0) html += '<li>📊 Quality Issues: ' + data.categories.quality + '</li>';
                if (data.categories.style > 0) html += '<li>✨ Style Issues: ' + data.categories.style + '</li>';
                html += '</ul>';
            }
            
            resultDiv.innerHTML = html;
            resultDiv.classList.add('show');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Interactive home page with code analysis interface"""
    return render_template_string(
        HOME_TEMPLATE, 
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
        samples=SAMPLE_CODES
    )

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "patchpro-demo",
        "version": "0.1.0"
    })

@app.route('/api/info')
def info():
    """Project information endpoint"""
    return jsonify({
        "name": "patchpro-demo",
        "description": "Interactive demo for PatchPro - Live code analysis and quality checking",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "features": [
            "Live code analysis via web interface",
            "REST API for code quality checking",
            "Security vulnerability detection",
            "Code style and quality validation",
            "Sample code examples",
            "CI/CD integration ready"
        ],
        "repository": "https://github.com/A3copilotprogram/patchpro-demo-repo",
        "endpoints": {
            "GET /": "Interactive web interface",
            "GET /api/health": "Health check",
            "GET /api/info": "This endpoint",
            "POST /api/analyze": "Analyze Python code",
            "GET /api/samples": "Get sample problematic code",
            "GET /api/demo-files": "Analyze demo repository files"
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """
    Analyze Python code for quality issues
    Expected JSON: {"code": "python code string"}
    Returns: {"issues": [...], "total_issues": int}
    """
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({"error": "Missing 'code' field in request"}), 400
        
        code = data['code']
        if not code.strip():
            return jsonify({"error": "Code cannot be empty"}), 400
        
        # Create a temporary file to analyze
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run Ruff analysis
            result = subprocess.run(
                ['python', '-m', 'ruff', 'check', '--output-format=json', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Parse results (Ruff returns JSON even on errors)
            issues = []
            if result.stdout:
                try:
                    issues = json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass
            
            # Categorize issues
            categories = {
                'security': 0,
                'quality': 0,
                'style': 0
            }
            
            formatted_issues = []
            for issue in issues:
                code = issue.get('code', 'UNKNOWN')
                
                # Categorize by code prefix
                if code.startswith('S'):  # Security
                    categories['security'] += 1
                elif code.startswith(('F', 'E')):  # Errors and Syntax
                    categories['quality'] += 1
                else:  # Style and others
                    categories['style'] += 1
                
                formatted_issues.append({
                    'code': code,
                    'message': issue.get('message', 'No message'),
                    'line': issue.get('location', {}).get('row', 0),
                    'column': issue.get('location', {}).get('column', 0),
                    'severity': 'error' if code.startswith('F') else 'warning'
                })
            
            return jsonify({
                "success": True,
                "total_issues": len(formatted_issues),
                "issues": formatted_issues,
                "categories": categories,
                "analyzer": "Ruff"
            })
            
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
                
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Analysis timed out"}), 408
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/api/samples')
def get_samples():
    """Get sample code snippets with common issues"""
    return jsonify({
        "samples": SAMPLE_CODES,
        "description": "Sample code snippets demonstrating common issues"
    })

@app.route('/api/demo-files')
def analyze_demo_files():
    """Analyze the demo files in the repository"""
    try:
        # Look for Python files in the current directory
        demo_files = ['example.py', 'ci_test.py', 'test_sample.py']
        results = {}
        
        for filename in demo_files:
            if os.path.exists(filename):
                try:
                    result = subprocess.run(
                        ['python', '-m', 'ruff', 'check', '--output-format=json', filename],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    issues = []
                    if result.stdout:
                        try:
                            issues = json.loads(result.stdout)
                        except json.JSONDecodeError:
                            pass
                    
                    results[filename] = {
                        "total_issues": len(issues),
                        "issues": issues[:5]  # Limit to first 5 issues
                    }
                except Exception as e:
                    results[filename] = {"error": str(e)}
            else:
                results[filename] = {"error": "File not found"}
        
        return jsonify({
            "success": True,
            "files_analyzed": len(results),
            "results": results,
            "note": "Showing first 5 issues per file"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to analyze demo files: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
