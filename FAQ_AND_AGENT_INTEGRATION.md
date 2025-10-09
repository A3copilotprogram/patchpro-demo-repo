# PatchPro Demo - FAQ & Troubleshooting Guide

**Date:** October 7, 2025  
**Status:** Production Ready

---

## 🔍 Issue: External Repo URL Fetching

### Problem
Getting `Error: Server error: 500` when trying to fetch code from external repositories, but prebuilt examples work fine.

### Possible Causes & Solutions

#### 1. **GitHub Rate Limiting**

**Symptom:** Works initially, then fails after several requests

**Check Render Logs:**
```
Dashboard → Your Service → Logs
Look for: "403 Forbidden" or "rate limit exceeded"
```

**Solution:**
Add GitHub token for authenticated requests (higher rate limits):

```python
# In app.py, update fetch_from_url endpoint:
headers = {
    'User-Agent': 'PatchPro-Demo/1.0'
}

# Optional: Add GitHub token for higher rate limits
github_token = os.environ.get('GITHUB_TOKEN')
if github_token and 'github.com' in url:
    headers['Authorization'] = f'token {github_token}'

response = requests.get(url, timeout=10, headers=headers)
```

#### 2. **URL Format Issues**

**Common Problems:**

❌ **Wrong URL Format:**
```
https://github.com/user/repo                    # Repo home page
https://github.com/user/repo/tree/main/file.py  # Tree view
```

✅ **Correct URL Formats:**
```
https://github.com/user/repo/blob/main/file.py          # Blob view (auto-converted)
https://raw.githubusercontent.com/user/repo/main/file.py # Raw content
https://gist.github.com/user/gist-id                     # Gist
https://pastebin.com/raw/paste-id                        # Pastebin raw
```

**Our converter handles:**
- ✅ `github.com/*/blob/*` → `raw.githubusercontent.com`
- ✅ `gist.github.com/*` → adds `/raw`
- ✅ `pastebin.com/*` → adds `/raw/`

#### 3. **Private Repositories**

**Problem:** Can't access private repos

**Why:** App can't authenticate to private repos

**Solutions:**
1. Use public repos for demos
2. Add GitHub token (see solution #1)
3. Clone repo locally and paste code directly

#### 4. **Large Files**

**Limit:** 1MB per file

**Error:** "File too large (max 1MB)"

**Solution:**
- Use smaller files
- Or extract specific functions/classes

#### 5. **Non-Python Files**

**Problem:** Trying to analyze non-Python code

**Solution:**
- Ensure URL points to `.py` file
- Or paste Python code directly in editor

---

## 🔍 Debugging Steps

### Step 1: Check Render Logs

```
1. Go to Render Dashboard
2. Click your service: patchpro-demo
3. Click "Logs" tab
4. Look for error messages around the time of failure
```

**Common Log Messages:**

```python
# ✅ Success
"GET /api/fetch-url - 200"
"Fetched 1234 bytes from https://..."

# ❌ Rate Limit
"403 Forbidden - API rate limit exceeded"

# ❌ Timeout
"requests.exceptions.Timeout"

# ❌ Not Found
"404 Not Found - File doesn't exist"
```

### Step 2: Test URL Directly

```bash
# Test if URL is accessible
curl -I "https://raw.githubusercontent.com/user/repo/main/file.py"

# Should return:
# HTTP/2 200
# content-type: text/plain; charset=utf-8
```

### Step 3: Check Browser Console

```javascript
// Open F12 Developer Tools
// Look for detailed error:
fetch('/api/fetch-url', {...})
  .catch(err => console.error(err))

// Check Network tab:
// - Request payload
// - Response body
// - Status code
```

### Step 4: Test with Known Good URLs

**Working Examples:**

```
# Python file from public repo
https://raw.githubusercontent.com/psf/requests/main/src/requests/__init__.py

# GitHub Gist
https://gist.github.com/username/gist-id/raw

# Pastebin
https://pastebin.com/raw/paste-id
```

---

## 🤖 PatchPro Agent Integration

### Current Implementation vs Full PatchPro

#### What This Demo Does ✅

```python
def generate_ai_fixes(code, issues, api_key):
    """
    Uses OpenAI GPT-4 directly for code analysis
    """
    client = OpenAI(api_key=api_key)
    
    # Send issues to GPT-4
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[...],
        max_tokens=2000
    )
    
    return response.choices[0].message.content
```

**This is:**
- ✅ AI-powered code analysis
- ✅ Intelligent fix suggestions
- ✅ Uses GPT-4
- ❌ NOT using PatchPro's agent system
- ❌ NOT using PatchPro's specialized models
- ❌ NOT integrated with main PatchPro repo

#### What Full PatchPro Does 🚀

The main PatchPro repository (with agent system) has:

```python
# From patchpro main repo
from patchpro.agent import PatchProAgent
from patchpro.models import CodeAnalysisModel

agent = PatchProAgent(
    model=CodeAnalysisModel(),
    config=agent_config
)

# Agent-based analysis with specialized models
result = agent.analyze_and_patch(
    code=code,
    context=context,
    patch_strategy='intelligent'
)
```

**Features in Full PatchPro:**
- ✅ Specialized agent architecture
- ✅ Context-aware patching
- ✅ Multi-step reasoning
- ✅ Custom-trained models
- ✅ Advanced patch strategies
- ✅ CI/CD integration
- ✅ Historical analysis

---

## 🔗 Integrating with PatchPro Main Repo

### Option 1: Direct Integration (Recommended for Production)

**Add PatchPro as dependency:**

```python
# requirements.txt
patchpro>=1.0.0  # Add main PatchPro package

# app.py
from patchpro import PatchProAgent
from patchpro.config import load_config

# Initialize PatchPro agent
patchpro_config = load_config()
agent = PatchProAgent(config=patchpro_config)

def generate_ai_fixes(code, issues, api_key):
    """
    Use PatchPro agent instead of direct OpenAI
    """
    try:
        # Use PatchPro's agent system
        result = agent.analyze(
            code=code,
            issues=issues,
            api_key=api_key
        )
        
        return result.formatted_output()
    except Exception as e:
        # Fallback to direct OpenAI if needed
        return direct_openai_analysis(code, issues, api_key)
```

### Option 2: API Integration

**Call PatchPro service API:**

```python
# If PatchPro has an API service
def generate_ai_fixes(code, issues, api_key):
    """
    Call PatchPro API service
    """
    response = requests.post(
        'https://patchpro-api.example.com/analyze',
        json={
            'code': code,
            'issues': issues
        },
        headers={'Authorization': f'Bearer {api_key}'}
    )
    
    return response.json()['analysis']
```

### Option 3: Microservice Architecture

```
┌─────────────────┐
│ PatchPro Demo   │
│ (This App)      │
└────────┬────────┘
         │
         │ HTTP/gRPC
         │
┌────────▼────────┐
│ PatchPro Agent  │
│ Service         │
│ (Main Repo)     │
└────────┬────────┘
         │
         │ Calls
         │
┌────────▼────────┐
│ OpenAI / Models │
└─────────────────┘
```

---

## 🧪 Validating PatchPro Agent Integration

### Current Demo (No Agent)

**Test:**
```bash
# Check if using PatchPro agent
curl -X POST https://your-app.onrender.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "test", "api_key": "sk-..."}'

# Look in response for:
"analyzer": "PatchPro AI"  # Generic name
```

**Check code:**
```python
# Current implementation
from openai import OpenAI  # Direct OpenAI
client = OpenAI(api_key=api_key)  # No PatchPro agent
```

### With PatchPro Agent Integration

**Test:**
```bash
# After integration
curl -X POST https://your-app.onrender.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "test", "api_key": "sk-..."}'

# Look for:
"analyzer": "PatchPro Agent v1.0"
"agent_used": true
"patch_strategy": "intelligent"
```

**Check code:**
```python
# With agent integration
from patchpro.agent import PatchProAgent  # PatchPro's agent
agent = PatchProAgent(...)
result = agent.analyze(...)  # Uses agent system
```

---

## 🎯 Recommended Next Steps

### For Demo/Testing (Current State)

**Keep as-is:**
- ✅ Works great for demos
- ✅ Shows AI capabilities
- ✅ Easy to understand
- ✅ No complex dependencies
- ✅ Fast deployment

**Purpose:** Showcase the concept of AI-powered code analysis

### For Production Integration

**Integrate PatchPro agent:**

1. **Add PatchPro dependency:**
   ```bash
   # If PatchPro is on PyPI
   pip install patchpro
   
   # Or from GitHub
   pip install git+https://github.com/A3copilotprogram/patchpro.git
   ```

2. **Update app.py:**
   ```python
   from patchpro import PatchProAgent
   
   agent = PatchProAgent(config=your_config)
   
   def generate_ai_fixes(code, issues, api_key):
       return agent.analyze_and_fix(code, issues, api_key)
   ```

3. **Update response:**
   ```python
   response_data = {
       "analyzer": "PatchPro Agent",
       "agent_version": agent.version,
       "agent_used": True,
       # ... rest of response
   }
   ```

---

## 📊 Comparison Table

| Feature | Current Demo | With PatchPro Agent |
|---------|-------------|---------------------|
| **AI Analysis** | ✅ Yes (GPT-4) | ✅ Yes (Specialized) |
| **Agent System** | ❌ No | ✅ Yes |
| **Custom Models** | ❌ No | ✅ Yes |
| **Context Awareness** | ⚠️ Limited | ✅ Advanced |
| **Patch Strategies** | ⚠️ Basic | ✅ Multiple |
| **Easy Deployment** | ✅ Very Easy | ⚠️ Moderate |
| **Dependencies** | ⚠️ Minimal | ⚠️ More Complex |
| **Best For** | Demos, Testing | Production Use |

---

## 🔍 How to Check What You're Using

### Check 1: Dependencies

```bash
# Look at requirements.txt
cat requirements.txt

# If you see:
openai>=1.50.0  # ← Direct OpenAI (current)

# Or:
patchpro>=1.0.0  # ← PatchPro agent (integrated)
```

### Check 2: Code Imports

```python
# Current demo approach
from openai import OpenAI  # Direct OpenAI

# PatchPro agent approach
from patchpro.agent import PatchProAgent  # PatchPro system
```

### Check 3: Response Format

```json
// Current demo
{
  "analyzer": "PatchPro AI",
  "ai_powered": true
}

// With PatchPro agent
{
  "analyzer": "PatchPro Agent v1.0",
  "agent_used": true,
  "agent_metadata": {
    "model": "patchpro-specialized-v1",
    "strategy": "intelligent",
    "confidence": 0.95
  }
}
```

---

## 🎯 Quick Decision Guide

### Use Current Demo If:
- ✅ You want a **quick demo** of AI code analysis
- ✅ You want **easy deployment** (no complex setup)
- ✅ You want to **showcase the concept**
- ✅ You don't need PatchPro's specialized features

### Integrate PatchPro Agent If:
- ✅ You need **production-grade** analysis
- ✅ You want **specialized models** for code patching
- ✅ You need **context-aware** patch strategies
- ✅ You want full **PatchPro capabilities**
- ✅ You're building on top of PatchPro's ecosystem

---

## 🚀 Implementation Guide for Agent Integration

### Step 1: Check PatchPro Main Repo

```bash
# Clone PatchPro main repo
git clone https://github.com/A3copilotprogram/patchpro.git
cd patchpro

# Check if it's packaged
ls setup.py pyproject.toml

# Check documentation
cat README.md
cat docs/integration.md
```

### Step 2: Install PatchPro

```bash
# If available on PyPI
pip install patchpro

# Or from source
cd patchpro
pip install -e .
```

### Step 3: Update Demo App

```python
# Add to app.py
try:
    from patchpro.agent import PatchProAgent
    PATCHPRO_AVAILABLE = True
except ImportError:
    PATCHPRO_AVAILABLE = False

def generate_ai_fixes(code, issues, api_key):
    if PATCHPRO_AVAILABLE:
        # Use PatchPro agent
        agent = PatchProAgent(api_key=api_key)
        return agent.analyze_and_fix(code, issues)
    else:
        # Fallback to direct OpenAI
        return direct_openai_analysis(code, issues, api_key)
```

### Step 4: Update Requirements

```txt
# requirements.txt
Flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
openai>=1.50.0
ruff==0.5.7

# Add PatchPro
patchpro>=1.0.0  # If available
# or
# git+https://github.com/A3copilotprogram/patchpro.git@main
```

### Step 5: Deploy and Test

```bash
git add requirements.txt app.py
git commit -m "feat: Integrate PatchPro agent system"
git push origin feature/render-deployment

# Render will auto-deploy
# Test with: curl https://your-app.onrender.com/api/analyze
```

---

## 📝 Summary

### Current Status
- ✅ **Demo works** with prebuilt examples
- ⚠️ **External URLs** may fail due to rate limits or format issues
- ⚠️ **Not using PatchPro agent** - using direct OpenAI calls

### To Fix URL Issues
1. Check Render logs for specific errors
2. Test URLs in browser/curl first
3. Ensure proper URL format (raw content URLs)
4. Consider adding GitHub token for rate limits

### To Validate Agent Integration
1. Check if `patchpro` package is imported
2. Look for `PatchProAgent` usage in code
3. Check response format for agent metadata
4. Currently: **NOT using agent** (direct OpenAI)

### To Integrate PatchPro Agent
1. Add `patchpro` to requirements.txt
2. Import and use `PatchProAgent`
3. Update code to use agent.analyze()
4. Test and validate responses

---

**Need Help?**
- Check Render logs for specific errors
- Test URLs with curl/browser
- Review PatchPro main repo for integration docs
- Ask about specific error messages for targeted help!
