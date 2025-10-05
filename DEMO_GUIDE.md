# PatchPro Demo Repository

This repository demonstrates how to use PatchPro in a real-world project. It contains intentionally flawed code that PatchPro can analyze and fix.

## Quick Start

### 1. Prerequisites
- Python 3.12+
- uv package manager
- OpenAI API key

### 2. Setup
```bash
# Clone this repository
git clone <repo-url>
cd patchpro-demo-repo

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
```

### 3. Run PatchPro Analysis

```bash
# Run the complete PatchPro workflow (analysis + LLM patching)
python -m patchpro_bot.cli run-ci

# Or with custom settings
python -m patchpro_bot.cli run-ci --base-dir . --artifacts artifact --tools ruff --tools semgrep
```

For local development workflows, see the [Local Developer Guide](https://github.com/A3copilotprogram/patchpro-bot/blob/agent-dev/docs/LOCAL_DEVELOPER_GUIDE.md).

## What This Demo Contains

### Test Files with Intentional Issues

- **`example.py`** - Basic code with common issues:
  - Unused imports
  - Hardcoded passwords
  - Inefficient code patterns

- **`test_sample.py`** - Comprehensive test cases:
  - Security vulnerabilities
  - Performance issues
  - Style violations
  - Exception handling problems

### Analysis Configuration

- **`semgrep.yml`** - Security and quality rules
- **`pyproject.toml`** - Ruff linting configuration

## Expected Output

After running PatchPro, you'll get (in the `artifact/` or `patchpro-artifacts/` directory):

```
artifact/
├── analysis/                    # Raw analysis data
│   ├── ruff_output.json
│   ├── semgrep_output.json
│   └── normalized_findings.json # Merged and normalized findings
├── report.md                    # Comprehensive markdown report
├── patch_combined_*.diff        # AI-generated fixes (when OpenAI is configured)
├── patch_summary_*.md           # Summary of changes (when patches generated)
└── patchpro_enhanced.log       # Detailed execution logs
```

**Note:** Patch files are only generated when:
- OpenAI API key is configured (`OPENAI_API_KEY` environment variable)
- Findings are detected that the LLM can address
- The run-ci command completes the full pipeline

## Using in Your Own Project

### 1. Add PatchPro Configuration

Create or update your `pyproject.toml`:
```toml
[project]
name = "your-project"
version = "0.1.0"
requires-python = ">=3.8"
dependencies = []

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.ruff]
select = ["F", "E", "I", "N"]  # Configure rules as needed
```

### 2. Add GitHub Actions (Optional)

Copy `.github/workflows/patchpro.yml` to your repository and add your OpenAI API key as a GitHub secret named `OPENAI_API_KEY`.

### 3. Run Analysis

```bash
# Option 1: Use the integrated run-ci command (recommended)
# This runs analysis tools AND generates AI patches in one step
python -m patchpro_bot.cli run-ci --base-dir . --artifacts artifact

# Option 2: Just analyze without LLM patching
python -m patchpro_bot.cli analyze . --format table

# Option 3: Use new developer-friendly commands
python -m patchpro_bot.cli watch .              # Watch files and analyze on change
python -m patchpro_bot.cli diff-analyze main    # Analyze only changed lines vs main branch
python -m patchpro_bot.cli status               # Check project setup and configuration
```

See the [Local Developer Guide](https://github.com/A3copilotprogram/patchpro-bot/blob/agent-dev/docs/LOCAL_DEVELOPER_GUIDE.md) for comprehensive local usage patterns.

## Manual Analysis Steps (For Understanding)

If you want to understand what PatchPro does under the hood, the `run-ci` command now performs these steps automatically:

```bash
# 1. Run static analysis tools
mkdir -p artifact/analysis
ruff check --output-format json . > artifact/analysis/ruff_output.json || true
semgrep --config .semgrep.yml --json . > artifact/analysis/semgrep_output.json || true

# 2. The run-ci command automatically:
#    - Normalizes findings from both tools
#    - Runs LLM analysis to generate patches
#    - Creates comprehensive reports
python -m patchpro_bot.cli run-ci --base-dir . --artifacts artifact

# 3. Review outputs
cat artifact/report.md
cat artifact/patch_combined_*.diff  # If generated
```

**Note:** You no longer need to run analysis tools separately - `run-ci` handles everything!

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - Required for AI-generated patch fixes
- `PP_ARTIFACTS` - Artifact directory path (default: `artifact`)

### Local Development Configuration
Create a `.patchpro.toml` file in your project root for team-wide settings:

```toml
[analysis]
tools = ["ruff", "semgrep"]
fail_on_findings = false

[ruff]
config_file = "pyproject.toml"

[semgrep]
config_file = ".semgrep.yml"

[llm]
model = "gpt-4o-mini"
temperature = 0.3

[output]
artifact_dir = "artifact"
```

### Analysis Tools
- **Ruff** - Fast Python linter and formatter (v0.5.7+)
- **Semgrep** - Static analysis for security and quality (v1.84.0+)

## Understanding the Issues

### Security Issues
```python
# Hardcoded secrets (detected by Semgrep)
password = "hardcoded_password123"
api_key = "secret-api-key"
```

### Code Quality Issues
```python
# Unused imports (detected by Ruff)
import os, sys  # Multiple imports on one line

# Performance issues
numbers = [1, 2, 3, 4, 5]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))  # Could be list comprehension
```

### Style Issues
```python
# String formatting (detected by Ruff)
message = "Hello {}".format(name)  # Should use f-string
```

## Troubleshooting

### No API Key
If you see "OpenAI API key not provided":
1. Create `.env` file with `OPENAI_API_KEY=your-key`
2. Or export the environment variable: `export OPENAI_API_KEY=your-key`

### Python Version
If you see Python version errors:
1. Install Python 3.12+
2. Use `uv python install 3.12` if using uv

### No Analysis Files
If you see "No analysis files found":
1. Run the manual analysis steps above
2. Check that `artifact/analysis/` contains JSON files

## Next Steps

1. **Explore the generated patches** - Review AI-generated fixes in `artifact/patch_combined_*.diff`
2. **Apply patches selectively** - Use `git apply` to apply fixes you approve
3. **Customize rules** - Modify `semgrep.yml` and `pyproject.toml` for your needs
4. **Integrate with CI** - Use the GitHub Actions workflow (see `.github/workflows/patchpro.yml`)
5. **Local development** - Set up git hooks and watch mode for real-time analysis (see [Local Developer Guide](https://github.com/A3copilotprogram/patchpro-bot/blob/agent-dev/docs/LOCAL_DEVELOPER_GUIDE.md))

## Additional Resources

- **[Local Developer Guide](https://github.com/A3copilotprogram/patchpro-bot/blob/agent-dev/docs/LOCAL_DEVELOPER_GUIDE.md)** - Comprehensive guide for using PatchPro locally with git hooks, watch mode, and IDE integration
- **[GitHub Actions Setup](https://github.com/A3copilotprogram/patchpro-bot/blob/agent-dev/docs/GITHUB_ACTIONS.md)** - Complete CI/CD integration guide
- **[Configuration Reference](https://github.com/A3copilotprogram/patchpro-bot/blob/agent-dev/docs/CONFIGURATION.md)** - All available settings and options