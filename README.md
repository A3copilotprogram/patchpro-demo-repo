# patchpro-demo-repo

PatchPro demo repository showcasing AI-powered code analysis and fixes.

## Quick Demo

```bash
# 1. Setup
git clone <this-repo>
cd patchpro-demo-repo
echo "OPENAI_API_KEY=your-openai-key" > .env

# 2. Run PatchPro
uv run --with /path/to/patchpro-bot-agent-dev python -m patchpro_bot.run_ci

# 3. See the magic ✨
cat artifact/report.md              # Analysis report
cat artifact/patch_combined_*.diff  # AI-generated fixes
```

## What You'll See

- **10+ code issues** automatically detected
- **AI-generated fixes** for security, performance, and style issues  
- **Production-ready patches** you can apply to your code
- **Comprehensive reports** with metrics and recommendations

**📖 For detailed instructions:** See [DEMO_GUIDE.md](./DEMO_GUIDE.md)

**🔧 For development setup:** See the [main repository](https://github.com/A3copilotprogram/patchpro-bot)
