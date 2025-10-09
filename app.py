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
import re
from pathlib import Path
try:
    import requests
except ImportError:
    requests = None
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Import PatchPro Bot integration
try:
    from patchpro_integration import (
        PatchProIntegration,
        is_patchpro_available,
        get_integration_status
    )
    PATCHPRO_INTEGRATION_AVAILABLE = True
except ImportError:
    PATCHPRO_INTEGRATION_AVAILABLE = False
    print("[WARNING] PatchPro Bot integration not available - using direct OpenAI fallback")

# Import Repository Analyzer
try:
    from repo_analyzer import RepositoryAnalyzer
    REPO_ANALYZER_AVAILABLE = True
except ImportError:
    REPO_ANALYZER_AVAILABLE = False
    print("[WARNING] Repository analyzer not available")

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

def generate_ai_fixes(code, issues, api_key):
    """
    Generate AI-powered fixes for code issues
    Uses PatchPro Bot's agentic system if available, falls back to direct OpenAI
    """
    if not api_key or not api_key.startswith('sk-'):
        return "Invalid API key format. OpenAI keys start with 'sk-'"
    
    try:
        # Try PatchPro Bot integration first
        if PATCHPRO_INTEGRATION_AVAILABLE and is_patchpro_available():
            print("[INFO] Using PatchPro Bot agentic system for analysis")
            integration = PatchProIntegration(api_key)
            result = integration.analyze_and_fix_sync(code, issues)
            
            if result.get('success'):
                # Format PatchPro result
                analysis = result.get('analysis', '')
                fixed_code = result.get('fixed_code', code)
                
                output = f"""FIXED CODE:
```python
{fixed_code}
```

{analysis}

---
✨ **Powered by PatchPro Bot Agentic System**
- Attempts: {result.get('agent_metadata', {}).get('attempts', 1)}
- Success Rate: {result.get('agent_metadata', {}).get('success_rate', 1.0):.1%}
- Strategy: {result.get('agent_metadata', {}).get('strategy', 'unified_diff')}
"""
                return output
            else:
                print(f"[WARNING] PatchPro Bot failed: {result.get('error')}, falling back to direct OpenAI")
                # Fall through to OpenAI fallback
        
        # Fallback to direct OpenAI
        print("[INFO] Using direct OpenAI for analysis (fallback mode)")
        return generate_ai_fixes_fallback(code, issues, api_key)
    
    except Exception as e:
        print(f"[ERROR] AI fix generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error generating AI fixes: {str(e)}"


def generate_ai_fixes_fallback(code, issues, api_key):
    """
    Fallback: Direct OpenAI integration (original implementation)
    """
    if not OpenAI:
        return "OpenAI library not available"
    
    try:
        # Initialize OpenAI client
        client = OpenAI(
            api_key=api_key,
            max_retries=2,
            timeout=30.0
        )
    except Exception as e:
        error_msg = str(e)
        if 'proxies' in error_msg.lower():
            return "OpenAI client initialization failed. Please ensure you're using the latest openai library."
        return f"Error initializing OpenAI client: {error_msg}"
    
    # Format issues for the prompt
    issues_summary = "\n".join([
        f"- Line {issue['line']}: {issue['code']} - {issue['message']}"
        for issue in issues[:10]  # Limit to first 10 issues
    ])
    
    prompt = f"""You are PatchPro, an AI-powered code analysis and fixing assistant. 

Analyze this Python code and fix the following issues:

{issues_summary}

Original Code:
```python
{code}
```

Provide:
1. Fixed code (complete, working version)
2. Brief explanation of changes made
3. Any additional recommendations

Format your response as:
FIXED CODE:
```python
[your fixed code here]
```

CHANGES MADE:
[list of changes]

RECOMMENDATIONS:
[optional recommendations]
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are PatchPro, an expert Python code analyzer and fixer. Provide clean, working code fixes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        return f"{result}\n\n---\n⚡ **Direct OpenAI Mode** (PatchPro Bot not available)"
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

# Error handlers to return JSON instead of HTML
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "status": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "status": 500}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if hasattr(e, 'code'):
        return jsonify({"error": str(e), "status": e.code}), e.code
    # Handle non-HTTP exceptions
    return jsonify({"error": f"An error occurred: {str(e)}", "status": 500}), 500

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
        .url-input-section {
            margin: 20px 0;
            padding: 20px;
            background: #e8f4fd;
            border-radius: 8px;
            border: 2px solid #61affe;
        }
        .url-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #61affe;
            border-radius: 8px;
            font-size: 14px;
            margin: 10px 0;
            box-sizing: border-box;
            font-family: 'Courier New', monospace;
        }
        .url-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .or-divider {
            text-align: center;
            margin: 20px 0;
            position: relative;
        }
        .or-divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #ddd;
            z-index: 0;
        }
        .or-divider span {
            background: #fff3cd;
            padding: 0 15px;
            position: relative;
            z-index: 1;
            color: #856404;
            font-weight: bold;
        }
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
                    <p class="subtitle">AI-Powered Code Analysis & Automatic Fixing - Bring Your Own API Key</p>
        <div class="badge">Status: Running</div>
        <div class="badge">Python {{ python_version }}</div>
        <div class="badge">AI-Powered</div>
        
        <div class="section interactive-section">
            <h2>🚀 Try It Live!</h2>
            <p>Paste your Python code, provide a URL, or load a sample to see <strong>PatchPro's AI</strong> in action. Get intelligent analysis with automated fix suggestions powered by OpenAI GPT-4.</p>
            
            <div style="margin: 15px 0;">
                <button class="btn btn-sample" onclick="loadSample('security')">Load Security Example</button>
                <button class="btn btn-sample" onclick="loadSample('quality')">Load Quality Example</button>
                <button class="btn btn-sample" onclick="loadSample('style')">Load Style Example</button>
            </div>
            
            <div class="url-input-section">
                <h3 style="margin-top: 0;">📎 Fetch Code from URL</h3>
                <p style="font-size: 14px; color: #666;">
                    Enter a URL to a Python file (GitHub, raw.githubusercontent.com, Pastebin, etc.)
                </p>
                <input 
                    type="text" 
                    id="urlInput" 
                    class="url-input" 
                    placeholder="https://raw.githubusercontent.com/user/repo/main/file.py"
                />
                <button class="btn" onclick="fetchFromUrl()">📥 Fetch Code from URL</button>
                <div style="margin-top: 10px; font-size: 12px; color: #666;">
                    <strong>Supported:</strong> GitHub, raw URLs, gists, pastebin (raw), direct file URLs
                </div>
            </div>
            
            <div class="or-divider">
                <span>OR PASTE DIRECTLY</span>
            </div>
            
            <textarea id="codeInput" placeholder="# Paste your Python code here...
# Example:
import os

password = 'hardcoded123'  # This will be flagged!

def my_function():
    unused_var = 'test'
    print('Hello')
"></textarea>
            
            <div style="margin: 15px 0; padding: 15px; background: #f5f5f5; border-radius: 8px; border: 1px solid #ddd;">
                <label style="display: block; margin-bottom: 8px; font-size: 14px; font-weight: bold;">
                    🔑 OpenAI API Key (Required for AI Analysis)
                </label>
                <input type="password" id="apiKeyInput" placeholder="sk-..." 
                    style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-family: monospace; font-size: 13px;">
                <small style="color: #666; display: block; margin-top: 5px;">
                    💡 Your API key is only used for this analysis and is never stored. Get one at <a href="https://platform.openai.com/api-keys" target="_blank">platform.openai.com</a>
                </small>
            </div>
            
            <button class="btn" onclick="analyzeCode()">🔍 Analyze Code</button>
            <button class="btn" onclick="clearResults()">Clear</button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p id="loadingText">🤖 AI analyzing your code...</p>
            </div>
            
            <div class="result" id="result"></div>
        </div>

        <div class="section interactive-section">
            <h2>🏢 Analyze Entire Repository</h2>
            <p>Analyze complete GitHub repositories for comprehensive code quality assessment. Get insights across all Python files in a project.</p>
            
            <div style="margin: 15px 0; padding: 15px; background: #e3f2fd; border-radius: 8px; border: 2px solid #2196f3;">
                <h3 style="margin-top: 0;">📊 Repository Analysis</h3>
                <input 
                    type="text" 
                    id="repoUrlInput" 
                    class="url-input" 
                    placeholder="https://github.com/owner/repository"
                    style="border-color: #2196f3;"
                />
                <div style="margin: 10px 0;">
                    <label style="margin-right: 15px;">
                        <strong>Branch:</strong>
                    </label>
                    <input 
                        type="text" 
                        id="repoBranchInput" 
                        placeholder="main" 
                        style="width: 150px; padding: 8px; border: 1px solid #2196f3; border-radius: 4px;"
                    />
                    <small style="color: #666; margin-left: 10px;">Leave empty for default branch</small>
                </div>
                <button class="btn" onclick="analyzeRepository()" style="background: #2196f3;">
                    📊 Analyze Repository
                </button>
                <button class="btn" onclick="getRepoInfo()" style="background: #4caf50;">
                    ℹ️ Get Repo Info
                </button>
                <div style="margin-top: 10px; font-size: 12px; color: #666;">
                    <strong>Features:</strong> Analyzes up to 50 Python files, categorizes issues, shows top problematic files
                    <br><strong>Note:</strong> Analysis may take 30-60 seconds for large repositories
                </div>
            </div>
            
            <div class="loading" id="repoLoading" style="display: none;">
                <div class="spinner"></div>
                <p id="repoLoadingText">📦 Cloning and analyzing repository...</p>
            </div>
            
            <div class="result" id="repoResult" style="display: none;"></div>
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
                <span class="method post">POST</span>
                <code>/api/fetch-url</code>
                <p>Fetch Python code from URL - send JSON with <code>{"url": "https://..."}</code></p>
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
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/analyze-repo</code>
                <p>Analyze entire GitHub repository - send JSON with <code>{"repo_url": "https://github.com/owner/repo", "branch": "main"}</code></p>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <code>/api/repo-info</code>
                <p>Get repository information - send JSON with <code>{"repo_url": "https://github.com/owner/repo"}</code></p>
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
            document.getElementById('urlInput').value = '';
            clearResults();
        }
        
        function clearResults() {
            document.getElementById('result').classList.remove('show');
            document.getElementById('result').innerHTML = '';
        }
        
        async function fetchFromUrl() {
            const url = document.getElementById('urlInput').value.trim();
            if (!url) {
                alert('Please enter a URL!');
                return;
            }
            
            // Validate URL format
            try {
                new URL(url);
            } catch (e) {
                alert('Please enter a valid URL!');
                return;
            }
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            
            try {
                const response = await fetch('/api/fetch-url', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url })
                });
                
                // Check if response is ok
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status} ${response.statusText}`);
                }
                
                // Check content type
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    const text = await response.text();
                    console.error('Received non-JSON response:', text.substring(0, 200));
                    throw new Error('Server returned invalid response. Expected JSON but got HTML.');
                }
                
                const data = await response.json();
                
                if (data.error) {
                    alert('Error fetching code: ' + data.error);
                    document.getElementById('loading').classList.remove('show');
                    return;
                }
                
                // Populate the code editor with fetched code
                document.getElementById('codeInput').value = data.code;
                document.getElementById('loading').classList.remove('show');
                
                // Show success message
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `
                    <div class="issue info">
                        <strong>✅ Code Fetched Successfully!</strong><br>
                        Source: ${data.source || url}<br>
                        Size: ${data.size || 'Unknown'} characters<br>
                        <small>Click "Analyze Code" to check for issues.</small>
                    </div>
                `;
                resultDiv.classList.add('show');
                
            } catch (error) {
                alert('Failed to fetch code: ' + error.message);
                document.getElementById('loading').classList.remove('show');
            }
        }
        
        async function analyzeCode() {
            const code = document.getElementById('codeInput').value;
            if (!code.trim()) {
                alert('Please enter some code to analyze!');
                return;
            }
            
            const apiKey = document.getElementById('apiKeyInput').value.trim();
            const loadingText = document.getElementById('loadingText');
            
            if (apiKey) {
                loadingText.textContent = '🤖 AI analyzing your code and generating fixes... (this may take 10-15 seconds)';
            } else {
                loadingText.textContent = 'Analyzing your code... (Add API key for AI-powered fixes)';
            }
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        code: code,
                        api_key: apiKey
                    })
                });
                
                // Check if response is ok
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status} ${response.statusText}`);
                }
                
                // Check content type before parsing
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    const text = await response.text();
                    console.error('Received non-JSON response:', text.substring(0, 200));
                    throw new Error('Server returned invalid response. Expected JSON but got HTML. Check console for details.');
                }
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                console.error('Analysis error:', error);
                document.getElementById('result').innerHTML = 
                    '<div class="issue"><strong>Error:</strong> ' + error.message + '<br><small>Check browser console for more details.</small></div>';
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
            
            let html = '<h3>📊 PatchPro AI Analysis Results</h3>';
            html += '<p><strong>Analyzer:</strong> ' + (data.analyzer || 'PatchPro AI') + '</p>';
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
            
            // Display AI-generated analysis and fixes
            if (data.ai_analysis) {
                html += '<div style="margin-top: 30px; padding: 20px; background: #e8f5e9; border-radius: 8px; border: 2px solid #4caf50;">';
                html += '<h3 style="margin-top: 0;">🤖 PatchPro AI Analysis & Fixes</h3>';
                html += '<pre style="background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; max-height: 600px;">';
                html += escapeHtml(data.ai_analysis);
                html += '</pre>';
                html += '<p style="font-size: 12px; color: #666; margin-bottom: 0;">✨ <strong>AI-powered by OpenAI GPT-4</strong> | ⚠️ Review and test all suggestions before use</p>';
                html += '</div>';
            } else if (data.ai_powered === false && data.ai_error) {
                html += '<div class="issue warning" style="margin-top: 20px;">';
                html += '<strong>🤖 AI Analysis:</strong> ' + data.ai_error;
                html += '<br><small>Enter your OpenAI API key above to enable AI-powered fixes and suggestions.</small>';
                html += '</div>';
            }
            
            resultDiv.innerHTML = html;
            resultDiv.classList.add('show');
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Repository Analysis Functions
        async function analyzeRepository() {
            const repoUrl = document.getElementById('repoUrlInput').value.trim();
            const branch = document.getElementById('repoBranchInput').value.trim() || 'main';
            
            if (!repoUrl) {
                alert('Please enter a repository URL!');
                return;
            }
            
            if (!repoUrl.includes('github.com')) {
                alert('Only GitHub repositories are supported!');
                return;
            }
            
            document.getElementById('repoLoading').style.display = 'block';
            document.getElementById('repoResult').style.display = 'none';
            document.getElementById('repoLoadingText').textContent = 'Cloning and analyzing repository... (this may take 30-60 seconds)';
            
            try {
                const response = await fetch('/api/analyze-repo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        repo_url: repoUrl,
                        branch: branch
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status} ${response.statusText}`);
                }
                
                const data = await response.json();
                displayRepositoryResults(data);
                
            } catch (error) {
                console.error('Repository analysis error:', error);
                document.getElementById('repoResult').innerHTML = 
                    '<div class="issue"><strong>Error:</strong> ' + error.message + '</div>';
                document.getElementById('repoResult').style.display = 'block';
            } finally {
                document.getElementById('repoLoading').style.display = 'none';
            }
        }
        
        async function getRepoInfo() {
            const repoUrl = document.getElementById('repoUrlInput').value.trim();
            
            if (!repoUrl) {
                alert('Please enter a repository URL!');
                return;
            }
            
            document.getElementById('repoLoading').style.display = 'block';
            document.getElementById('repoResult').style.display = 'none';
            document.getElementById('repoLoadingText').textContent = 'Fetching repository information...';
            
            try {
                const response = await fetch('/api/repo-info', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ repo_url: repoUrl })
                });
                
                const data = await response.json();
                displayRepositoryInfo(data);
                
            } catch (error) {
                console.error('Repository info error:', error);
                document.getElementById('repoResult').innerHTML = 
                    '<div class="issue"><strong>Error:</strong> ' + error.message + '</div>';
                document.getElementById('repoResult').style.display = 'block';
            } finally {
                document.getElementById('repoLoading').style.display = 'none';
            }
        }
        
        function displayRepositoryResults(data) {
            const resultDiv = document.getElementById('repoResult');
            
            if (data.error) {
                resultDiv.innerHTML = '<div class="issue"><strong>Error:</strong> ' + data.error + '</div>';
                resultDiv.style.display = 'block';
                return;
            }
            
            let html = '<h3>📊 Repository Analysis Results</h3>';
            
            // Repository info
            html += '<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">';
            html += '<h4 style="margin-top: 0;">📦 Repository Overview</h4>';
            html += '<p><strong>URL:</strong> ' + data.repository.url + '</p>';
            html += '<p><strong>Branch:</strong> ' + data.repository.branch + '</p>';
            html += '<p><strong>Files Analyzed:</strong> ' + data.repository.files_analyzed + ' Python files</p>';
            html += '<p><strong>Total Size:</strong> ' + Math.round(data.repository.total_size_bytes / 1024) + ' KB</p>';
            html += '<p><strong>Total Lines:</strong> ' + data.repository.total_lines.toLocaleString() + '</p>';
            html += '<p><strong>Analysis Time:</strong> ' + data.analysis_time + ' seconds</p>';
            html += '</div>';
            
            // Analysis summary
            html += '<div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0;">';
            html += '<h4 style="margin-top: 0;">🔍 Analysis Summary</h4>';
            html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">';
            
            // Left column
            html += '<div>';
            html += '<p><strong>Total Issues:</strong> ' + data.analysis.total_issues + '</p>';
            html += '<p><strong>Files with Issues:</strong> ' + data.analysis.files_with_issues + ' / ' + data.repository.files_analyzed + '</p>';
            html += '<p><strong>Issue Density:</strong> ' + data.analysis.issue_density + ' per 1000 lines</p>';
            html += '</div>';
            
            // Right column
            html += '<div>';
            html += '<p><strong>Quality Grade:</strong> <span style="font-size: 1.2em; font-weight: bold; color: ' + getGradeColor(data.analysis.quality_grade) + ';">' + data.analysis.quality_grade + '</span></p>';
            if (data.analysis.file_stats) {
                html += '<p><strong>Clean Files:</strong> ' + data.analysis.file_stats.without_issues + '</p>';
                html += '<p><strong>Failed Analysis:</strong> ' + data.analysis.file_stats.analysis_failed + '</p>';
            }
            html += '</div>';
            html += '</div>';

            html += '<h5>📊 Issue Categories:</h5><ul>';
            if (data.analysis.categories.security > 0) html += '<li>🔒 Security Issues: ' + data.analysis.categories.security + '</li>';
            if (data.analysis.categories.quality > 0) html += '<li>📊 Quality Issues: ' + data.analysis.categories.quality + '</li>';
            if (data.analysis.categories.style > 0) html += '<li>✨ Style Issues: ' + data.analysis.categories.style + '</li>';
            html += '</ul></div>';
            
            // Directory analysis
            if (data.directory_analysis && Object.keys(data.directory_analysis).length > 0) {
                html += '<div style="background: #e8f4fd; padding: 15px; border-radius: 8px; margin: 15px 0;">';
                html += '<h4 style="margin-top: 0;">📁 Directory Analysis</h4>';
                Object.entries(data.directory_analysis).forEach(([dir, stats]) => {
                    html += '<div style="margin: 8px 0; padding: 8px; background: white; border-radius: 4px;">';
                    html += '<strong>' + dir + '/</strong> - ' + stats.files + ' files, ' + stats.issues + ' issues';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            // Top problematic files
            if (data.top_problematic_files && data.top_problematic_files.length > 0) {
                html += '<div style="background: #ffebee; padding: 15px; border-radius: 8px; margin: 15px 0;">';
                html += '<h4 style="margin-top: 0;">🚨 Top Problematic Files</h4>';
                data.top_problematic_files.forEach((file, index) => {
                    html += '<div style="margin: 10px 0; padding: 12px; background: white; border-radius: 4px; border-left: 4px solid ' + getSeverityColor(file.issues) + ';">';
                    html += '<div style="display: flex; justify-content: space-between; align-items: center;">';
                    html += '<strong>' + file.file + '</strong>';
                    html += '<span style="background: ' + getSeverityColor(file.issues) + '; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">' + file.issues + ' issues</span>';
                    html += '</div>';
                    html += '<div style="margin-top: 5px; font-size: 13px; color: #666;">';
                    html += 'Lines: ' + file.lines + ' | Density: ' + file.issue_density + '% | ';
                    if (file.categories.security > 0) html += '🔒 ' + file.categories.security + ' ';
                    if (file.categories.quality > 0) html += '📊 ' + file.categories.quality + ' ';
                    if (file.categories.style > 0) html += '✨ ' + file.categories.style + ' ';
                    html += '</div>';
                    html += '</div>';
                });
                html += '</div>';
            }
            
            // Warnings and limitations
            if (data.files_truncated) {
                html += '<div class="issue warning" style="margin-top: 20px;">';
                html += '<strong>⚠️ Analysis Limited:</strong> Only the first ' + data.max_files_limit + ' files were analyzed. ';
                html += 'Large repositories may have additional files not included in this analysis.';
                html += '</div>';
            }
            
            html += '<div style="margin-top: 20px; font-size: 12px; color: #666;">';
            html += '<p><strong>Note:</strong> This analysis shows static code issues found by Ruff. ';
            html += 'Consider running additional tools for comprehensive security analysis.</p>';
            html += '</div>';
            
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
        }
        
        function displayRepositoryInfo(data) {
            const resultDiv = document.getElementById('repoResult');
            
            if (data.error) {
                resultDiv.innerHTML = '<div class="issue"><strong>Error:</strong> ' + data.error + '</div>';
                resultDiv.style.display = 'block';
                return;
            }
            
            let html = '<h3>ℹ️ Repository Information</h3>';
            
            html += '<div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">';
            html += '<h4 style="margin-top: 0;">📦 ' + (data.name || 'Repository') + '</h4>';
            if (data.description) html += '<p><strong>Description:</strong> ' + data.description + '</p>';
            if (data.language) html += '<p><strong>Primary Language:</strong> ' + data.language + '</p>';
            if (data.stars !== undefined) html += '<p><strong>Stars:</strong> ' + data.stars.toLocaleString() + ' ⭐</p>';
            if (data.forks !== undefined) html += '<p><strong>Forks:</strong> ' + data.forks.toLocaleString() + ' 🍴</p>';
            if (data.size !== undefined) html += '<p><strong>Size:</strong> ' + data.size + ' KB</p>';
            if (data.default_branch) html += '<p><strong>Default Branch:</strong> ' + data.default_branch + '</p>';
            if (data.last_updated) {
                const date = new Date(data.last_updated).toLocaleDateString();
                html += '<p><strong>Last Updated:</strong> ' + date + '</p>';
            }
            html += '</div>';
            
            html += '<div style="margin-top: 15px;">';
            html += '<button class="btn" onclick="analyzeRepository()" style="background: #2196f3;">📊 Analyze This Repository</button>';
            html += '</div>';
            
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
        }
        
        function getGradeColor(grade) {
            const colors = {
                'A+': '#4caf50',
                'A': '#8bc34a', 
                'B': '#ffeb3b',
                'C': '#ff9800',
                'D': '#f44336'
            };
            return colors[grade] || '#666';
        }
        
        function getSeverityColor(issueCount) {
            if (issueCount >= 10) return '#f44336';  // Red
            if (issueCount >= 5) return '#ff9800';   // Orange  
            if (issueCount >= 1) return '#ffeb3b';   // Yellow
            return '#4caf50';  // Green
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
    features = [
        "Live code analysis via web interface",
        "REST API for code quality checking",
        "Security vulnerability detection",
        "Code style and quality validation",
        "Sample code examples",
        "CI/CD integration ready"
    ]
    
    endpoints = {
        "GET /": "Interactive web interface",
        "GET /api/health": "Health check",
        "GET /api/info": "This endpoint",
        "POST /api/analyze": "Analyze Python code",
        "POST /api/fetch-url": "Fetch code from URL",
        "GET /api/samples": "Get sample problematic code",
        "GET /api/demo-files": "Analyze demo repository files"
    }
    
    # Add repository analysis features if available
    if REPO_ANALYZER_AVAILABLE:
        features.extend([
            "Full repository analysis",
            "GitHub repository cloning and analysis",
            "Multi-file code quality assessment",
            "Repository-wide issue categorization"
        ])
        endpoints.update({
            "POST /api/analyze-repo": "Analyze entire GitHub repository",
            "POST /api/repo-info": "Get repository information"
        })
    
    return jsonify({
        "name": "patchpro-demo",
        "description": "Interactive demo for PatchPro - Live code analysis and repository assessment",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "features": features,
        "repository": "https://github.com/A3copilotprogram/patchpro-demo-repo",
        "endpoints": endpoints,
        "capabilities": {
            "single_file_analysis": True,
            "repository_analysis": REPO_ANALYZER_AVAILABLE,
            "ai_powered_fixes": bool(OpenAI),
            "patchpro_integration": PATCHPRO_INTEGRATION_AVAILABLE
        }
    })

@app.route('/api/fetch-url', methods=['POST'])
def fetch_from_url():
    """
    Fetch Python code from a URL
    Expected JSON: {"url": "https://..."}
    Returns: {"code": "fetched code", "source": "url", "size": int}
    """
    if not requests:
        return jsonify({"error": "requests library not available"}), 500
    
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "Missing 'url' field in request"}), 400
        
        url = data['url'].strip()
        if not url:
            return jsonify({"error": "URL cannot be empty"}), 400
        
        # Log original URL for debugging
        print(f"[DEBUG] Original URL: {url}")
        
        # Convert GitHub URLs to raw URLs
        url = convert_to_raw_url(url)
        print(f"[DEBUG] Converted URL: {url}")
        
        # Fetch the content
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'PatchPro-Demo/1.0'
            })
            print(f"[DEBUG] Response status: {response.status_code}")
            response.raise_for_status()
            
            code = response.text
            
            # Basic validation - check if it looks like Python code
            if not code.strip():
                return jsonify({"error": "Fetched content is empty"}), 400
            
            # Check if it's likely Python code (basic heuristic)
            if len(code) > 1000000:  # 1MB limit
                return jsonify({"error": "File too large (max 1MB)"}), 400
            
            return jsonify({
                "success": True,
                "code": code,
                "source": url,
                "size": len(code),
                "lines": len(code.splitlines())
            })
            
        except requests.Timeout:
            print(f"[ERROR] Timeout fetching URL: {url}")
            return jsonify({"error": "Request timed out (max 10 seconds)"}), 408
        except requests.HTTPError as e:
            print(f"[ERROR] HTTP error: {e.response.status_code} for URL: {url}")
            return jsonify({"error": f"HTTP error: {e.response.status_code} - {e.response.reason}"}), 400
        except requests.RequestException as e:
            print(f"[ERROR] Request exception: {str(e)} for URL: {url}")
            return jsonify({"error": f"Failed to fetch URL: {str(e)}"}), 400
            
    except Exception as e:
        print(f"[ERROR] Unexpected error in fetch_from_url: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

def convert_to_raw_url(url):
    """Convert GitHub URLs to raw content URLs"""
    # GitHub blob URL to raw URL
    if 'github.com' in url and '/blob/' in url:
        url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    
    # GitHub gist URL to raw URL
    if 'gist.github.com' in url and '/raw/' not in url:
        # Try to append /raw if it's a gist
        if url.endswith('.py') or url.count('/') >= 4:
            url = url + '/raw' if not url.endswith('/') else url + 'raw'
    
    # Pastebin to raw
    if 'pastebin.com' in url and '/raw/' not in url:
        url = url.replace('pastebin.com/', 'pastebin.com/raw/')
    
    return url

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """
    Analyze Python code using PatchPro AI-powered analysis
    Expected JSON: {"code": "python code string"}
    Returns: {"issues": [...], "total_issues": int, "ai_analysis": "...", "ai_fixes": "..."}
    """
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({"error": "Missing 'code' field in request"}), 400
        
        code = data['code']
        api_key = data.get('api_key', '').strip()  # Get API key from request
        
        if not code.strip():
            return jsonify({"error": "Code cannot be empty"}), 400
        
        # Create a temporary file to analyze
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run Ruff analysis
            result = subprocess.run(
                ['python3', '-m', 'ruff', 'check', '--output-format=json', temp_file],
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
            
            response_data = {
                "success": True,
                "total_issues": len(formatted_issues),
                "issues": formatted_issues,
                "categories": categories,
                "analyzer": "PatchPro AI",
                "agent_used": False,  # Will be updated if PatchPro Bot is used
                "patchpro_status": get_integration_status() if PATCHPRO_INTEGRATION_AVAILABLE else None
            }
            
            # Always generate AI analysis if issues found and OpenAI is available
            if formatted_issues and OpenAI and api_key:
                try:
                    ai_analysis = generate_ai_fixes(code, formatted_issues, api_key)
                    if ai_analysis and not ai_analysis.startswith("Error"):
                        response_data['ai_analysis'] = ai_analysis
                        response_data['ai_powered'] = True
                        # Check if PatchPro Bot was actually used
                        if PATCHPRO_INTEGRATION_AVAILABLE and is_patchpro_available():
                            response_data['agent_used'] = True
                    else:
                        response_data['ai_error'] = ai_analysis or "Failed to generate AI analysis"
                        response_data['ai_powered'] = False
                except Exception as e:
                    response_data['ai_analysis'] = None
                    response_data['ai_error'] = f"AI analysis unavailable: {str(e)}"
                    response_data['ai_powered'] = False
            elif formatted_issues and not api_key:
                response_data['ai_powered'] = False
                response_data['ai_analysis'] = None
                response_data['ai_error'] = "Enter your OpenAI API key above to enable AI-powered fixes"
            else:
                response_data['ai_powered'] = False
                response_data['ai_analysis'] = None
            
            return jsonify(response_data)
            
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

@app.route('/api/analyze-repo', methods=['POST'])
def analyze_repository():
    """
    Analyze an entire GitHub repository
    Expected JSON: {"repo_url": "https://github.com/owner/repo", "branch": "main"}
    Returns: Comprehensive repository analysis
    """
    if not REPO_ANALYZER_AVAILABLE:
        return jsonify({
            "error": "Repository analyzer not available",
            "note": "This feature requires the repo_analyzer module"
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'repo_url' not in data:
            return jsonify({"error": "Missing 'repo_url' field in request"}), 400
        
        repo_url = data['repo_url'].strip()
        branch = data.get('branch', 'main')
        
        if not repo_url:
            return jsonify({"error": "Repository URL cannot be empty"}), 400
        
        # Validate GitHub URL
        if 'github.com' not in repo_url:
            return jsonify({"error": "Only GitHub repositories are supported"}), 400
        
        # Initialize analyzer
        analyzer = RepositoryAnalyzer(max_files=50, max_file_size=100000)
        
        # Perform analysis
        result = analyzer.analyze_repository(repo_url, branch)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Repository analysis failed: {str(e)}"}), 500

@app.route('/api/repo-info', methods=['POST'])
def get_repository_info():
    """
    Get basic repository information
    Expected JSON: {"repo_url": "https://github.com/owner/repo"}
    Returns: Repository metadata
    """
    if not REPO_ANALYZER_AVAILABLE:
        return jsonify({
            "error": "Repository analyzer not available"
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'repo_url' not in data:
            return jsonify({"error": "Missing 'repo_url' field in request"}), 400
        
        repo_url = data['repo_url'].strip()
        
        if not repo_url:
            return jsonify({"error": "Repository URL cannot be empty"}), 400
        
        # Initialize analyzer
        analyzer = RepositoryAnalyzer()
        
        # Get repository info
        result = analyzer.get_repository_info(repo_url)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Failed to get repository info: {str(e)}"}), 500

@app.route('/api/status')
def status():
    """API endpoint to check service status and PatchPro Bot integration"""
    patchpro_status = get_integration_status() if PATCHPRO_INTEGRATION_AVAILABLE else {
        'available': False,
        'version': None,
        'features': {}
    }
    
    return jsonify({
        'status': 'healthy',
        'service': 'PatchPro Demo',
        'features': ['ruff_analysis', 'ai_powered_fixes', 'url_fetching'],
        'patchpro_bot': patchpro_status
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

