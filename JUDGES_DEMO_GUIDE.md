# 🛡️ PatchPro: See It in Action

## 🎯 Quick Demo Options

### Option 1: Watch Real CI/CD in Action (Recommended)
**See PatchPro running live in GitHub Actions:**

📋 **Step-by-step:**
1. 🔗 **[View Live Workflow Runs](https://github.com/A3copilotprogram/patchpro-demo-repo-waigi-ci-test-demo/actions)**
2. Click any recent "PatchPro Agent-Dev" workflow
3. Click "Run PatchPro analyze-pr" step to see full output
4. Scroll through to see:
   - ✅ Code analysis with Ruff + Semgrep  
   - ✅ AI patch generation with GPT-4o-mini
   - ✅ Git validation and telemetry
   - ✅ PR comment posting

**What you'll see:**
- Real vulnerability detection 
- AI-powered patch generation
- Self-correction attempts
- Comprehensive telemetry
- PR integration

### Option 2: Interactive Demo (Zero Setup)
**Try it yourself in browser:**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/A3copilotprogram/patchpro-demo-repo-waigi-ci-test-demo?quickstart=1)

1. Click the button above
2. Wait 2-3 minutes for setup
3. Run: `./demo-real-workflow.sh`

### Option 3: Create Your Own PR
**Trigger PatchPro yourself:**

1. 🍴 Fork this repository
2. 🔧 Edit any `.py` file (introduce a security issue)
3. 📝 Create a Pull Request
4. 🤖 Watch PatchPro analyze and comment automatically

## 🎬 Recent Demo Runs

**Live examples you can view right now:**

- 🔗 [Latest Workflow Run](https://github.com/A3copilotprogram/patchpro-demo-repo-waigi-ci-test-demo/actions/runs/latest) 
- 🔗 [Example PR with PatchPro Comments](https://github.com/A3copilotprogram/patchpro-demo-repo-waigi-ci-test-demo/pulls)
- 🔗 [Download Artifacts](https://github.com/A3copilotprogram/patchpro-demo-repo-waigi-ci-test-demo/actions) (patches, traces, reports)

## 📊 What PatchPro Does

**In the GitHub Action, you'll see:**

1. **Code Analysis** 
   ```bash
   python -m patchpro_bot.cli analyze-pr --base origin/main --head HEAD --with-llm
   ```

2. **AI Patch Generation**
   - GPT-4o-mini analyzes findings
   - Generates production-ready unified diffs
   - Validates with `git apply --check`

3. **PR Integration**
   - Posts detailed analysis comment
   - Uploads artifacts (patches, traces, reports)
   - Shows telemetry and performance metrics

4. **Self-Learning**
   - Captures traces in SQLite database
   - Records prompt/response pairs for ML training
   - Tracks success/failure patterns

## 🚀 Key Features Demonstrated

- ✅ **Multi-Tool Analysis**: Ruff + Semgrep integration
- ✅ **AI-Powered Patches**: GPT-4o-mini generates fixes
- ✅ **Git Validation**: Every patch tested before delivery
- ✅ **Self-Learning**: SQLite traces for continuous improvement
- ✅ **CI/CD Integration**: Seamless GitHub Actions workflow
- ✅ **PR Comments**: Actionable insights posted automatically

## 🏆 Built for Andela GenAI Mastery Program 2025

**Team PLG_5** | [patchpro.ai](https://patchpro.ai) | [Documentation](https://github.com/A3copilotprogram/patchpro-bot)