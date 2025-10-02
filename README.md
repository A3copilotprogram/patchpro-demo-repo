# patchpro-demo-repo
<<<<<<< HEAD

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
=======
PatchPro demo repository (seed bugs + CI)

This is a minimal Python repository to test PatchPro Bot end-to-end.

## Structure

- `example.py` — Simple Python file with intentional lint and security issues
- `.github/workflows/patchpro.yml` — CI workflow to run PatchPro Bot
- `semgrep.yml` — Example Semgrep rules
- `pyproject.toml` — Python project config

## How to Use

1. Fork this repo and the main patchpro-bot repo.
2. Set the `OPENAI_API_KEY` secret in your fork.
3. Open a pull request or push to main — the PatchPro workflow will run and comment with a patch report.

## Example: `example.py`

```python
import os, sys

def add(a, b):
    password = "supersecret"  # Hardcoded password (Semgrep)
    return a + b
```

## Example: `semgrep.yml`

See the included `semgrep.yml` for custom rules.

---

This repo is for demo/testing only. Use it to validate PatchPro Bot end-to-end in CI.
>>>>>>> 7ac79b9 (chore: update workflow and docs for PatchPro demo)
