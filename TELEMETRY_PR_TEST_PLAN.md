# Telemetry PR Flow Test Plan

## Objective
Complete **Phase 1** of the Evaluation Framework Milestone by validating that telemetry infrastructure works in CI/CD environment (GitHub Actions).

## What We're Testing

### 1. Telemetry in CI Environment
- ✅ Traces captured when PatchPro runs in GitHub Actions
- ✅ SQLite database (`traces.db`) created with proper structure
- ✅ JSON trace files generated for each patch attempt
- ✅ Costs, latency, tokens tracked correctly
- ✅ Validation results recorded (success/failure)

### 2. Agentic Mode in PR Flow
- ✅ Feedback loop works in CI (retry on failures)
- ✅ Self-correction generates higher quality patches
- ✅ LLM sees validation errors and improves
- ✅ Retry logic respects `agentic_max_retries = 3`

### 3. CI Integration
- ✅ `analyze-pr` command runs correctly
- ✅ Changed files detected via `git diff`
- ✅ Patches uploaded as artifacts
- ✅ PR comments posted with results
- ✅ Build doesn't fail on findings (--no-exit-code)

## Setup Changes

### New Workflow File: `.github/workflows/patchpro-agent-dev-test.yml`

**Key Changes from old `patchpro.yml`:**

| Old (Sprint-0) | New (Agent-Dev with Telemetry) |
|----------------|-------------------------------|
| `ref: main` | `ref: agent-dev` |
| `run_ci.py` | `analyze-pr` command |
| No agentic mode | `enable_agentic_mode = true` |
| No telemetry | Telemetry enabled by default |
| Basic artifacts | Includes `traces.db` + JSON traces |

**Configuration via `.patchpro.toml`:**
```toml
[agent]
enable_agentic_mode = true
agentic_max_retries = 3
agentic_enable_planning = true

[llm]
model = "gpt-4o-mini"
temperature = 0.1
max_tokens = 8192
```

## Test Procedure

### Step 1: Create Test Branch with Issues

```bash
cd /opt/andela/genai/patchpro-demo-repo

# Create test branch
git checkout -b test-telemetry-pr-flow-001

# Add a file with intentional linting issues
cat > test_code_quality.py << 'EOF'
import os, sys, json

def process_data(data):
    result = []
    for item in data:
        if item['status'] == 'active':
            result.append(item)
    return result

class UserManager:
    def __init__(self, db):
        self.db = db
    
    def get_user(self, id):
        user = self.db.query(f"SELECT * FROM users WHERE id = {id}")
        return user

password = "admin123"  # Hardcoded secret
api_key = "sk-1234567890abcdef"

EOF

# Commit and push
git add test_code_quality.py
git commit -m "test: add file with quality issues for telemetry validation"
git push origin test-telemetry-pr-flow-001
```

### Step 2: Open Pull Request

1. Go to GitHub: `https://github.com/{owner}/patchpro-demo-repo/pulls`
2. Click "New Pull Request"
3. Base: `main`, Compare: `test-telemetry-pr-flow-001`
4. Title: "Test: Validate Telemetry in PR Flow (Phase 1)"
5. Description:
   ```markdown
   ## Purpose
   Testing Phase 1 of Evaluation Framework - Telemetry in CI
   
   ## Expected Behavior
   - PatchPro runs with `analyze-pr` command
   - Agentic mode enabled (self-correction)
   - Telemetry captures traces
   - Artifacts include `traces.db` and JSON files
   
   ## Issues in test_code_quality.py
   - Import violations (multiple imports on one line)
   - SQL injection vulnerability (f-string in query)
   - Hardcoded secrets
   - Missing docstrings
   - Unused imports
   ```
6. Create PR

### Step 3: Monitor GitHub Action

Watch the action run and verify:
- ✅ Workflow triggers (`patchpro-agent-dev-test.yml`)
- ✅ PatchPro analyzes `test_code_quality.py`
- ✅ Patches generated
- ✅ Telemetry summary appears in job output
- ✅ Artifacts uploaded

### Step 4: Download and Inspect Artifacts

```bash
# Download artifacts from GitHub Actions UI
# Or use gh CLI:
gh run download <run-id> -n patchpro-telemetry-artifacts

# Inspect telemetry data
ls -lh .patchpro/traces/

# Check database
sqlite3 .patchpro/traces/traces.db "SELECT COUNT(*) FROM traces;"
sqlite3 .patchpro/traces/traces.db "SELECT rule_id, status, cost FROM traces;"

# View trace JSON files
cat .patchpro/traces/trace_*.json | jq .
```

### Step 5: Validate Telemetry Data

Check that traces contain:
- ✅ **Finding context**: `rule_id`, `file`, `line`, `message`
- ✅ **LLM interaction**: `prompt`, `response`, `model`, `tokens`
- ✅ **Validation**: `validation_passed`, `git_apply_errors`
- ✅ **Performance**: `cost` ($), `latency_ms`, `timestamp`
- ✅ **Retry context**: `attempt_number`, `feedback_from_previous`

## Success Criteria

### Phase 1 Complete When:
- [ ] Telemetry works in CI (not just locally)
- [ ] Traces captured for all patch attempts
- [ ] SQLite database populated correctly
- [ ] JSON trace files human-readable
- [ ] Costs tracked (should be ~$0.001-0.005 per finding)
- [ ] Latency tracked (should be 2-10 seconds per finding)
- [ ] Agentic mode retries visible in traces
- [ ] Validation results recorded (success/failure)

## Next Steps After Validation

### If Successful ✅
1. **Mark Phase 1 complete** in `PATH_TO_MVP.md`
2. **Begin Week 2: Observability**
   - Build Streamlit trace viewer UI
   - Implement search/filter by rule_id, status, strategy
   - Display prompt + response + validation side-by-side
   - Export good examples to fine-tuning dataset

### If Issues Found ❌
1. **Debug telemetry in CI**
   - Check environment variables
   - Verify file paths in CI
   - Check database permissions
2. **Fix issues** and re-test
3. **Document learnings** in bug analysis

## Rollout Strategy

### This Test (Controlled)
- **Trigger**: Only on `test-telemetry-*` branches
- **Purpose**: Validate telemetry infrastructure
- **Risk**: Low (test branches only)

### After Validation (Production)
- **Update main workflow**: `patchpro.yml` → use `agent-dev`
- **Enable for all PRs**: Remove branch filter
- **Monitor costs**: Set budget alerts
- **Review traces weekly**: Identify improvement opportunities

## Cost Estimation

**Per PR Analysis:**
- 10-50 findings per PR (typical)
- ~$0.002 per finding with gpt-4o-mini
- ~$0.02-0.10 per PR total
- ~$2-10 per month for active repo

**Telemetry Storage:**
- SQLite database: ~100KB per 100 traces
- JSON traces: ~10KB per trace
- ~1MB per month for active repo

## Questions for Review

1. **Should telemetry be opt-in or opt-out in production?**
   - Currently: Always on in agentic mode
   - Consider: ENV variable to disable if needed

2. **How long to retain traces?**
   - Currently: 30 days in GitHub artifacts
   - Consider: Export to long-term storage?

3. **Should we upload traces.db to separate storage?**
   - Currently: Included in artifacts
   - Consider: S3/GCS for analytics?

4. **Privacy considerations?**
   - Traces include code snippets
   - Should we sanitize secrets before storing?

## References

- Evaluation Framework: `docs/PATH_TO_MVP.md`
- Architecture: `docs/ANALYSIS_ARCHITECTURE.md`
- Agentic Results: `docs/AGENTIC_FEEDBACK_LOOP_RESULTS.md`
- Telemetry Code: `src/patchpro_bot/telemetry.py`
