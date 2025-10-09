# Testing the Interactive Code Analysis Features

## 🎯 What to Test After Deployment

Your app now has **interactive code analysis**! Here's how to test it on Render.com.

---

## 🌐 Web Interface Testing

### 1. **Visit Your Deployed App**
```
https://your-app-name.onrender.com
```

### 2. **Test the Interactive Editor**

#### **Load Security Example**
1. Click the **"Load Security Example"** button
2. You should see code with hardcoded passwords
3. Click **"🔍 Analyze Code"**
4. Wait for results (should appear in ~1-2 seconds)
5. **Expected**: See issues about hardcoded credentials

#### **Load Quality Example**
1. Click **"Load Quality Example"**
2. You should see code with unused variables/imports
3. Click **"🔍 Analyze Code"**
4. **Expected**: See issues about unused code

#### **Load Style Example**
1. Click **"Load Style Example"**
2. You should see code with PEP 8 violations
3. Click **"🔍 Analyze Code"**
4. **Expected**: See formatting and style issues

### 3. **Test Custom Code**
Paste this code into the editor:
```python
import os
import sys

def login():
    password = "admin123"
    api_key = "sk-secret-key"
    unused_var = 42
    return password
```

Click "Analyze" - you should see:
- ✅ Unused imports (os, sys)
- ✅ Unused variable (unused_var)
- ✅ Potential issues flagged

---

## 🔧 API Testing

### Test Health Check
```bash
curl https://your-app-name.onrender.com/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "patchpro-demo",
  "version": "0.1.0"
}
```

### Test Info Endpoint
```bash
curl https://your-app-name.onrender.com/api/info
```

**Expected**: JSON with all endpoint information

### Test Code Analysis Endpoint
```bash
curl -X POST https://your-app-name.onrender.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "import os\npassword = \"secret123\"\nunused = 42"}'
```

**Expected Response:**
```json
{
  "success": true,
  "total_issues": 3,
  "issues": [
    {
      "code": "F401",
      "message": "'os' imported but unused",
      "line": 1,
      "column": 8,
      "severity": "error"
    },
    ...
  ],
  "categories": {
    "security": 0,
    "quality": 3,
    "style": 0
  },
  "analyzer": "Ruff"
}
```

### Test Samples Endpoint
```bash
curl https://your-app-name.onrender.com/api/samples
```

**Expected**: JSON with 3 sample code snippets

### Test Demo Files Analysis
```bash
curl https://your-app-name.onrender.com/api/demo-files
```

**Expected**: Analysis results for example.py, ci_test.py, test_sample.py

---

## ✅ Success Criteria

### Web Interface
- [ ] Page loads without errors
- [ ] All 3 sample buttons work
- [ ] Code editor accepts input
- [ ] Analyze button triggers analysis
- [ ] Loading spinner appears during analysis
- [ ] Results display with color-coded issues
- [ ] Issue counts match actual problems
- [ ] Clear button works

### API Endpoints
- [ ] `/api/health` returns 200 OK
- [ ] `/api/info` returns complete endpoint list
- [ ] `/api/analyze` accepts POST with code
- [ ] `/api/analyze` returns formatted issues
- [ ] `/api/samples` returns 3 samples
- [ ] `/api/demo-files` analyzes repository files

### Error Handling
- [ ] Empty code returns proper error
- [ ] Invalid JSON returns 400 error
- [ ] Missing 'code' field returns error message

---

## 🐛 Common Issues & Solutions

### Issue: "Ruff not found" Error
**Solution**: Render should auto-install from requirements.txt
- Check build logs in Render dashboard
- Verify requirements.txt includes `ruff==0.5.7`
- Trigger manual redeploy if needed

### Issue: Analysis Times Out
**Solution**: 10-second timeout is built in
- Try smaller code samples
- Check if Render service is under heavy load

### Issue: No Results Displayed
**Solution**: Check browser console for errors
- Open Developer Tools (F12)
- Look for JavaScript errors
- Check Network tab for API response

### Issue: 502 Bad Gateway
**Solution**: Service may be starting up
- Wait 30-60 seconds (cold start on free tier)
- Refresh the page
- Check Render dashboard for service status

---

## 📸 What Success Looks Like

### Home Page
✅ Modern purple gradient background  
✅ Interactive code editor (large textarea)  
✅ Three sample buttons (green)  
✅ Analyze and Clear buttons (purple/green)  
✅ API documentation section  
✅ Responsive design (works on mobile)  

### After Analysis
✅ Results section appears below editor  
✅ Issue count displayed  
✅ Color-coded issue cards:
- Red border = Errors
- Yellow border = Warnings  
- Blue border = Info
✅ Each issue shows: code, message, line, column  
✅ Category summary at bottom  

---

## 🔄 If You Need to Redeploy

### Option 1: Automatic (Recommended)
```bash
# Make any change and push
git add .
git commit -m "trigger redeploy"
git push origin feature/render-deployment
```
Render auto-deploys in ~1-2 minutes

### Option 2: Manual Redeploy
1. Go to Render Dashboard
2. Select your service
3. Click "Manual Deploy"
4. Select branch: `feature/render-deployment`
5. Click "Deploy"

---

## 📊 Performance Testing

### Expected Response Times
- **Health check**: < 100ms
- **Info endpoint**: < 100ms
- **Code analysis**: 500ms - 2s (depending on code size)
- **Sample loading**: Instant (client-side)

### Load Testing (Optional)
```bash
# Test 10 requests
for i in {1..10}; do
  curl -X POST https://your-app-name.onrender.com/api/analyze \
    -H "Content-Type: application/json" \
    -d '{"code": "import os"}' &
done
wait
```

---

## 🎓 Demo Script for Presentations

### 1. **Introduction** (30 seconds)
"This is PatchPro - an AI-powered code analysis tool. Let me show you how it works live."

### 2. **Load Security Example** (30 seconds)
"First, let's look at some code with security issues..."  
*Click Load Security Example*  
*Click Analyze*  
"See? It immediately detects hardcoded passwords and API keys."

### 3. **Load Quality Example** (30 seconds)
"Now let's check code quality..."  
*Click Load Quality Example*  
*Click Analyze*  
"It finds unused variables, imports, and dead code."

### 4. **Custom Code** (1 minute)
"You can paste any Python code. Let me show you..."  
*Paste custom problematic code*  
*Click Analyze*  
"Real-time analysis with detailed explanations."

### 5. **API Demo** (30 seconds)
"This also works as an API for integration..."  
*Show curl command or Postman*

**Total: ~3 minutes**

---

## 🚀 Next Steps After Testing

1. **Share the URL** with your team/users
2. **Update PR description** with live demo link
3. **Add screenshots** to documentation
4. **Merge to main** when ready
5. **Announce** the interactive demo!

---

## 💡 Tips for Best Experience

- ✅ Use **Chrome or Firefox** for best compatibility
- ✅ Test on **mobile devices** too (responsive design)
- ✅ **Clear browser cache** if you see old version
- ✅ Check **Render logs** if something doesn't work
- ✅ Use **sample codes first** to verify functionality

---

## 📞 Need Help?

If something doesn't work:
1. Check Render dashboard logs
2. Verify all files committed and pushed
3. Ensure requirements.txt has ruff==0.5.7
4. Try manual redeploy from Render
5. Check browser console for errors

---

**Ready to test? Visit your Render URL and start analyzing code! 🎉**
