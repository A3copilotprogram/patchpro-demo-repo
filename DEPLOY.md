# Deploying PatchPro Demo to Render.com

This guide walks you through deploying the PatchPro demo to Render.com.

## 📋 Prerequisites

- GitHub account
- Render.com account (free tier available)
- This repository pushed to GitHub

## 🚀 Quick Deploy

### Method 1: Using Render Blueprint (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment files"
   git push origin feature/add-requirements-txt
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click **"Apply"** to deploy

### Method 2: Manual Web Service Setup

1. **Push code to GitHub** (same as above)

2. **Create Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure:
     - **Name**: `patchpro-demo`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Plan**: Free (or choose paid plan)

3. **Click "Create Web Service"**

## 📁 Files Created for Deployment

| File | Purpose |
|------|---------|
| `app.py` | Flask web application with API endpoints |
| `requirements.txt` | Python dependencies (Flask, Gunicorn) |
| `render.yaml` | Render Blueprint configuration |
| `Procfile` | Process type definition |
| `runtime.txt` | Python version specification |
| `.python-version` | Python version for deployment |

## 🌐 What Gets Deployed

The deployment creates a simple web interface with:

- **Home Page** (`/`) - Project information and documentation
- **Health Check** (`/api/health`) - Service status endpoint
- **Info API** (`/api/info`) - Project metadata as JSON

## 🔐 Optional: Environment Variables

If you want to add the OpenAI API key for PatchPro features:

1. Go to your service in Render Dashboard
2. Navigate to **"Environment"** tab
3. Add:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key
   - Check **"Secret"** to hide the value

## 🔍 Testing Your Deployment

Once deployed, Render will provide a URL like:
```
https://patchpro-demo.onrender.com
```

Test the endpoints:
```bash
# Home page
curl https://patchpro-demo.onrender.com/

# Health check
curl https://patchpro-demo.onrender.com/api/health

# Project info
curl https://patchpro-demo.onrender.com/api/info
```

## 🐛 Troubleshooting

### Build Fails
- Check that `requirements.txt` is in the root directory
- Verify Python version compatibility (3.12)
- Review build logs in Render Dashboard

### Service Won't Start
- Check that `app.py` is in the root directory
- Verify the start command: `gunicorn app:app`
- Review service logs in Render Dashboard

### Import Errors
- Ensure all dependencies are in `requirements.txt`
- Check that Flask and Gunicorn versions are compatible

## 📊 Render Free Tier Limitations

- Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month free (enough for one service)
- Upgrade to paid plan for:
  - No sleep/downtime
  - Custom domains
  - More resources

## 🔄 Continuous Deployment

Render automatically redeploys when you push to your GitHub branch:

```bash
# Make changes
git add .
git commit -m "Update application"
git push origin feature/add-requirements-txt

# Render will automatically deploy the changes
```

## 📝 Next Steps

1. **Custom Domain**: Add your own domain in Render Dashboard
2. **Monitoring**: Enable health checks and notifications
3. **Scaling**: Upgrade plan for better performance
4. **Database**: Add PostgreSQL or Redis if needed
5. **Add Features**: Extend the Flask app with more endpoints

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## 💡 Tips

- Use environment variables for sensitive data
- Enable automatic deploys from your main branch
- Set up health check endpoints for monitoring
- Use Render's built-in SSL (HTTPS automatically enabled)
- Check logs regularly during initial deployment

---

**Need Help?** Check the [Render Community](https://community.render.com/) or the [Render Status Page](https://status.render.com/)
