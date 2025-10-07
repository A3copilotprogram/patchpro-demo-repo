"""
PatchPro Demo - Simple Web Interface
A minimal Flask application for Render.com deployment
"""
from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PatchPro Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .badge { 
            display: inline-block;
            padding: 5px 10px;
            background: #4CAF50;
            color: white;
            border-radius: 3px;
            margin: 5px;
        }
        .info { 
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 PatchPro Demo Repository</h1>
        <div class="badge">Status: Running</div>
        <div class="badge">Python {{ python_version }}</div>
        
        <div class="info">
            <h3>About This Project</h3>
            <p>This is a demo repository for <strong>PatchPro</strong> - an AI-powered code analysis and automatic fixing tool.</p>
            <p>The project demonstrates how PatchPro can detect and fix:</p>
            <ul>
                <li>Security vulnerabilities (hardcoded secrets)</li>
                <li>Code quality issues (unused imports, variables)</li>
                <li>Style violations (formatting issues)</li>
                <li>Performance problems</li>
            </ul>
        </div>

        <h3>API Endpoints</h3>
        <ul>
            <li><code>GET /</code> - This page</li>
            <li><code>GET /api/health</code> - Health check</li>
            <li><code>GET /api/info</code> - Project information</li>
        </ul>

        <h3>Repository</h3>
        <p>View the source code: <a href="https://github.com/A3copilotprogram/patchpro-demo-repo">GitHub</a></p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with project information"""
    import sys
    return render_template_string(HOME_TEMPLATE, python_version=f"{sys.version_info.major}.{sys.version_info.minor}")

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
        "description": "Demo repository for PatchPro CI testing",
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}",
        "features": [
            "Code quality analysis",
            "Security vulnerability detection",
            "AI-powered automatic fixes",
            "CI/CD integration"
        ],
        "repository": "https://github.com/A3copilotprogram/patchpro-demo-repo"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
