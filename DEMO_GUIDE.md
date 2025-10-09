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
# Run the complete PatchPro workflow
uv run --with /path/to/patchpro-bot-agent-dev python -m patchpro_bot.run_ci
```

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

After running PatchPro, you'll get:

```
artifact/
├── analysis/                    # Raw analysis data
│   ├── ruff_output.json
│   └── semgrep_output.json
├── report.md                    # Comprehensive report
├── patch_combined_*.diff        # AI-generated fixes
├── patch_summary_*.md           # Summary of changes
└── patchpro_enhanced.log       # Detailed logs
```

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
# In your project directory
uv run --with /path/to/patchpro-bot-agent-dev python -m patchpro_bot.run_ci
```

## Manual Analysis Steps

If you want to understand what PatchPro does:

```bash
# 1. Generate static analysis
mkdir -p artifact/analysis
ruff check --output-format json . > artifact/analysis/ruff_output.json || true
semgrep --config .semgrep.yml --json . > artifact/analysis/semgrep_output.json || true

# 2. Run PatchPro analysis
uv run --with /path/to/patchpro-bot-agent-dev python -m patchpro_bot.run_ci

# 3. Review outputs
cat artifact/report.md
cat artifact/patch_combined_*.diff
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - Required for AI-generated fixes
- `PP_ARTIFACTS` - Artifact directory path (default: `artifact`)

### Analysis Tools
- **Ruff** - Fast Python linter and formatter
- **Semgrep** - Static analysis for security and quality

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

1. **Explore the generated patches** - See how AI fixes the issues
2. **Apply patches selectively** - Review and apply fixes you want
3. **Customize rules** - Modify `semgrep.yml` and ruff configuration
4. **Integrate with CI** - Use the GitHub Actions workflow