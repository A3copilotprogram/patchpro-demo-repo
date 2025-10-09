# 🚀 Render.com Deployment Setup Guide

**Complete guide for deploying PatchPro Demo to Render.com**

---

## 📋 Prerequisites

- ✅ GitHub account with access to `A3copilotprogram/patchpro-demo-repo`
- ✅ Render.com account (free tier works great!)
- ✅ Branch `feature/render-deployment` pushed to GitHub

---

## 🎯 Two Deployment Methods

### Method 1: Blueprint (Automatic) ⭐ **RECOMMENDED**
Uses `render.yaml` for automatic configuration.

### Method 2: Manual Setup
Configure settings in Render dashboard.

---

## Method 1: Blueprint Deployment (Easiest!)

### Step 1: Connect to Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com

2. **Click "New +"**
   - Select **"Blueprint"**

3. **Connect Repository**
   - Click "Connect account" (if not already connected)
   - Authorize Render to access your GitHub
   - Select repository: `A3copilotprogram/patchpro-demo-repo`
   - Choose branch: `feature/render-deployment`

4. **Render Auto-Detects `render.yaml`**
   - Shows: "1 service found"
   - Service name: `patchpro-demo`
   - Type: Web Service
   - Click **"Apply"**

5. **Done!**
   - Render creates the service
   - Starts deploying automatically
   - Takes ~2-3 minutes

### What Gets Configured Automatically

From `render.yaml`:
```yaml
✅ Service name: patchpro-demo
✅ Runtime: Python
✅ Plan: Free
✅ Build command: pip install -r requirements.txt
✅ Start command: gunicorn app:app
✅ Python version: 3.12.0
✅ Port: 10000
```

---

## Method 2: Manual Setup

### Step 1: Create New Web Service

1. **Go to Render Dashboard**
   - https://dashboard.render.com

2. **Click "New +"**
   - Select **"Web Service"**

3. **Connect Repository**
   - Connect your GitHub account
   - Select: `A3copilotprogram/patchpro-demo-repo`
   - Branch: `feature/render-deployment`
   - Click **"Connect"**

### Step 2: Configure Service Settings

#### Basic Settings
```
Name: patchpro-demo
Region: Oregon (US West) or closest to you
Branch: feature/render-deployment
Runtime: Python 3
```

#### Build & Deploy
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

#### Environment
```
PYTHON_VERSION = 3.12.0
```

#### Plan
```
Plan: Free (or Starter for production)
```

### Step 3: Deploy

Click **"Create Web Service"**

Render will:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Start the app with Gunicorn
4. Provide a URL like: `https://patchpro-demo.onrender.com`

---

## 🔑 Environment Variables (Optional)

**You DON'T need to set any environment variables!** 

Your app now uses **user-provided API keys**, so no server-side configuration is needed.

### Optional: Fallback Server Key (Not Recommended)

If you want to provide a fallback API key for when users don't have their own:

1. **Go to your service** in Render Dashboard
2. **Click "Environment"** tab
3. **Add Environment Variable:**
   ```
   Key: OPENAI_API_KEY
   Value: sk-your-openai-api-key-here
   ```
4. **Click "Save Changes"**
5. Render will auto-redeploy

**Note:** This is NOT recommended because:
- ❌ Shared quota limits
- ❌ Costs come from your account
- ❌ Not scalable
- ✅ User-provided keys are better!

---

## 📊 Deployment Settings Reference

### Complete Configuration

| Setting | Value | Required? |
|---------|-------|-----------|
| **Service Name** | `patchpro-demo` | ✅ Yes |
| **Runtime** | Python 3 | ✅ Yes |
| **Branch** | `feature/render-deployment` | ✅ Yes |
| **Build Command** | `pip install -r requirements.txt` | ✅ Yes |
| **Start Command** | `gunicorn app:app` | ✅ Yes |
| **Python Version** | 3.12.0 | ✅ Yes (set via env var) |
| **Plan** | Free | ✅ Yes (can upgrade) |
| **Region** | Oregon (US West) | ⚙️ Optional |
| **Port** | 10000 | ⚙️ Auto-detected |
| **Environment Variables** | None needed! | ❌ No |

### Auto-Deploy Settings

```
✅ Auto-Deploy: Yes (enabled by default)
✅ Branch: feature/render-deployment
```

When you push to GitHub, Render automatically:
1. Detects the change
2. Pulls latest code
3. Rebuilds the app
4. Deploys with zero downtime

---

## 🎛️ Advanced Settings (Optional)

### Health Check

Render automatically monitors: `GET /api/health`

**Default Settings (you don't need to change):**
```
Health Check Path: /api/health
Response Code: 200
Timeout: 30 seconds
Interval: 30 seconds
```

### Build & Deploy Options

```
Auto-Deploy: Yes
Build Filter: Deploy on every push
```

### Scaling (Free Plan)

```
Instances: 1
RAM: 512 MB
CPU: 0.1 vCPU
```

### Custom Domains (Optional)

You can add custom domains in the "Settings" tab:
```
1. Go to "Settings"
2. Scroll to "Custom Domains"
3. Add your domain
4. Configure DNS as instructed
```

---

## 📁 Files Render Uses

### `requirements.txt`
```txt
Flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
openai>=1.50.0  ← Fixed version!
ruff==0.5.7
setuptools>=68
wheel
```

### `render.yaml` (Blueprint)
```yaml
services:
  - type: web
    name: patchpro-demo
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: PORT
        value: 10000
```

### `Procfile` (Alternative)
```
web: gunicorn app:app
```

### `runtime.txt` (Specifies Python version)
```
python-3.12.0
```

---

## 🧪 After Deployment

### 1. Wait for Build to Complete

Render Dashboard will show:
```
⏳ Building...
⏳ Deploying...
✅ Live
```

This takes ~2-3 minutes.

### 2. Get Your App URL

```
Your app will be available at:
https://patchpro-demo-XXXX.onrender.com

(XXXX is a random string Render assigns)
```

### 3. Test Your App

Visit the URL and:
1. ✅ Page loads
2. ✅ Enter some Python code
3. ✅ Enter your OpenAI API key (from your `.env` file)
4. ✅ Click "Analyze Code"
5. ✅ See AI-powered fixes!

---

## 🔍 Monitoring & Logs

### View Logs

1. **Go to your service** in Render Dashboard
2. **Click "Logs"** tab
3. See real-time logs:
   ```
   [INFO] Starting gunicorn 21.2.0
   [INFO] Listening at: http://0.0.0.0:10000
   [INFO] Using worker: sync
   [INFO] Booting worker
   ```

### Check Metrics

1. **Click "Metrics"** tab
2. See:
   - Request count
   - Response time
   - Memory usage
   - CPU usage

---

## 🐛 Troubleshooting

### Build Fails

**Check:**
1. `requirements.txt` has all dependencies
2. Python version is correct (3.12.0)
3. No syntax errors in `app.py`

**View Logs:**
- Click "Logs" tab
- Look for error messages

### App Doesn't Start

**Check:**
1. Start command is: `gunicorn app:app`
2. `app.py` exists at root
3. Flask app variable is named `app`

**Common Issues:**
```python
# ✅ Correct
app = Flask(__name__)

# ❌ Wrong
application = Flask(__name__)  # Gunicorn looks for 'app'
```

### API Doesn't Work

**Check:**
1. User entered valid OpenAI API key
2. Key starts with `sk-`
3. Check logs for errors

### OpenAI Error

**Now Fixed!** 
- Updated to `openai>=1.50.0`
- No more "proxies" error
- Should work perfectly

---

## ⚡ Performance Tips

### Free Plan Limitations

```
✅ Good for demos and testing
✅ SSL/HTTPS included
✅ Auto-deploy on push
⚠️  Sleeps after 15 min of inactivity
⚠️  Cold start: ~30 seconds
⚠️  512 MB RAM limit
```

### Upgrade to Starter Plan ($7/month)

Benefits:
```
✅ No sleeping
✅ Always instant response
✅ More RAM (512 MB → 2 GB)
✅ Better performance
✅ Custom domains
```

### Keep Free Plan Active

**Use cron-job.org to ping your app:**
```
1. Sign up at cron-job.org
2. Create job:
   URL: https://your-app.onrender.com/api/health
   Interval: Every 10 minutes
3. Keeps app awake during business hours
```

---

## 🔐 Security Best Practices

### What Render Does Automatically

```
✅ HTTPS/SSL certificate (free)
✅ Environment variable encryption
✅ DDoS protection
✅ Automatic security updates
```

### What You Should Do

```
✅ Use user-provided API keys (already implemented!)
✅ Don't commit secrets to GitHub (already in .gitignore)
✅ Keep dependencies updated
✅ Monitor logs for suspicious activity
```

---

## 🎯 Complete Setup Checklist

### Pre-Deployment
- [x] Code pushed to GitHub
- [x] `requirements.txt` has all dependencies
- [x] `render.yaml` configured
- [x] OpenAI library updated to >=1.50.0
- [x] `.env` in `.gitignore` (API key safe)

### Render Setup
- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Use Blueprint deployment (easiest)
- [ ] Wait for build to complete (~2 min)

### Post-Deployment
- [ ] Visit app URL
- [ ] Test code analysis (without API key)
- [ ] Test AI analysis (with your API key)
- [ ] Verify all features work
- [ ] Share URL with users!

### Optional
- [ ] Set up custom domain
- [ ] Configure health check monitoring
- [ ] Set up cron job to keep awake
- [ ] Upgrade to Starter plan (if needed)

---

## 📚 Quick Reference

### Important URLs

| What | URL |
|------|-----|
| Render Dashboard | https://dashboard.render.com |
| Your App | `https://patchpro-demo-XXXX.onrender.com` |
| GitHub Repo | https://github.com/A3copilotprogram/patchpro-demo-repo |
| OpenAI Keys | https://platform.openai.com/api-keys |

### Important Commands

```bash
# Push changes (triggers auto-deploy)
git push origin feature/render-deployment

# View local app
python app.py
# or
gunicorn app:app

# Test OpenAI locally
export OPENAI_API_KEY="sk-your-key"
python test_openai_fix.py
```

### Support Resources

- **Render Docs:** https://render.com/docs
- **Render Support:** support@render.com
- **Flask Docs:** https://flask.palletsprojects.com
- **OpenAI Docs:** https://platform.openai.com/docs

---

## 🎉 Summary

### What You Need to Do on Render.com:

**Absolutely Minimal Setup:**
```
1. Click "New +" → "Blueprint"
2. Connect GitHub repo: A3copilotprogram/patchpro-demo-repo
3. Branch: feature/render-deployment
4. Click "Apply"
5. Done! ✨
```

**No environment variables needed!**  
**No complex configuration!**  
**Just connect and deploy!**

### What Happens Automatically:

```
✅ Render reads render.yaml
✅ Installs Python 3.12
✅ Runs: pip install -r requirements.txt
✅ Installs: Flask, Gunicorn, OpenAI >=1.50.0, Ruff
✅ Starts: gunicorn app:app
✅ Provides: HTTPS URL
✅ Enables: Auto-deploy on git push
```

### Your App Will:

```
✅ Load instantly at provided URL
✅ Show interactive code editor
✅ Accept user-provided API keys
✅ Perform static analysis (Ruff)
✅ Generate AI fixes (GPT-4)
✅ Fetch code from GitHub URLs
✅ Work perfectly!
```

---

## 🚀 Ready to Deploy?

**Just do this:**

1. Go to: https://dashboard.render.com
2. Click: "New +" → "Blueprint"
3. Connect: `A3copilotprogram/patchpro-demo-repo`
4. Branch: `feature/render-deployment`
5. Click: "Apply"
6. Wait: ~2 minutes
7. Test: Visit your new URL!
8. Share: Send link to users!

**That's it! No other configuration needed!** 🎊

---

**Questions?** Check the troubleshooting section or Render's excellent docs at https://render.com/docs
