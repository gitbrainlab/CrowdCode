# CrowdCode Workflows Reference

> **Understanding and controlling GitHub Actions automation**

This document describes each GitHub Actions workflow that powers CrowdCode, including what they do, how to configure them, and **how to disable them safely**.

## Workflow Overview

CrowdCode uses 4 GitHub Actions workflows:

| Workflow | Schedule | Purpose | Can Disable? |
|----------|----------|---------|--------------|
| **Issue to PR** | Daily (2 AM UTC) | Generate PRs from feature requests | ✅ Yes |
| **Vote Counting** | Hourly | Count PatchPanel votes on PRs | ✅ Yes |
| **Feature Promotion** | Daily (6 AM UTC) | Merge approved features to main | ✅ Yes |
| **Branch Visibility** | Weekly (Sunday) | Update feature branch dashboard | ✅ Yes |

**Critical Principle**: Every workflow can be disabled. Human control is always maintained.

---

## 1. Issue to PR Generation

**File**: `.github/workflows/crowdcode-issue-to-pr.yml`

### Purpose

Scans for new feature request issues and generates pull requests with AI-generated code implementations.

**⚠️ Important**: AI-generated code is a PROPOSAL. It requires human review and voting before merge.

### Trigger Events

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2:00 AM UTC
  workflow_dispatch:      # Manual trigger (with dry-run option)
    inputs:
      dry_run:
        description: 'Dry run mode (no actual changes)'
        required: false
        default: 'false'
        type: boolean
```

**Triggers**:
- **Scheduled**: Runs daily at 2:00 AM UTC
- **Manual**: Can be triggered anytime via Actions tab or CLI

### What It Does

**Step-by-step process**:

1. **Checkout repository** - Gets latest code from main branch
2. **Setup Python** - Installs Python 3.11 runtime
3. **Install dependencies** - Installs `PyGithub` and `pyyaml` packages
4. **Generate PRs from Issues** - Runs `scripts/generate-feature-pr.py`:
   - Scans for issues labeled `crowdcode:feature-request`
   - Excludes issues already labeled `crowdcode:pending-pr`
   - Limits to `max_per_run` issues (default: 5)
   - For each issue:
     - Creates feature branch: `crowdcode/feature-{issue-number}-{slug}`
     - Generates code (placeholder in Phase 1, AI in Phase 2)
     - Commits code to feature branch
     - Opens pull request linked to issue
     - Adds labels: `crowdcode:ai-generated`, `crowdcode:voting`
     - Updates issue label to `crowdcode:pending-pr`
5. **Summary** - Generates workflow summary report

### Inputs

**Manual trigger inputs**:
- `dry_run` (boolean, default: `false`) - Preview actions without making changes

**Configuration** (`.github/crowdcode-config.yml`):
```yaml
issue_processing:
  max_per_run: 5  # Maximum issues to process per run
  labels:
    feature_request: "crowdcode:feature-request"
    pending_pr: "crowdcode:pending-pr"
    ai_generated: "crowdcode:ai-generated"
    voting: "crowdcode:voting"

ai_generation:
  enabled: true  # Enable/disable AI code generation
  model: "gpt-4"
  max_tokens: 4000
  timeout_seconds: 300
```

### Outputs

**Created artifacts**:
- Feature branches: `crowdcode/feature-{issue-number}-{slug}`
- Pull requests with AI-generated code
- Issue comments linking to PR
- Updated issue labels

**Workflow summary**:
- Number of issues processed
- PRs created successfully
- Any errors encountered

### Permissions Required

```yaml
permissions:
  issues: write         # Update issue labels and comments
  pull-requests: write  # Create pull requests
  contents: write       # Create branches and commits
```

### How to Disable

**Option 1: Delete workflow file** (complete removal)
```bash
rm .github/workflows/crowdcode-issue-to-pr.yml
git add .github/workflows/crowdcode-issue-to-pr.yml
git commit -m "Disable CrowdCode PR generation"
git push
```

**Option 2: Rename workflow file** (temporary disable, easy to re-enable)
```bash
mv .github/workflows/crowdcode-issue-to-pr.yml \
   .github/workflows/crowdcode-issue-to-pr.yml.disabled
git add .github/workflows/
git commit -m "Temporarily disable CrowdCode PR generation"
git push
```

**Option 3: Disable AI generation only** (keep manual PR creation)
Edit `.github/crowdcode-config.yml`:
```yaml
ai_generation:
  enabled: false  # Disable AI, keep workflow structure
```

**Option 4: Disable scheduled runs** (keep manual trigger)
Edit workflow file:
```yaml
on:
  # schedule:  # Comment out schedule
  #   - cron: '0 2 * * *'
  workflow_dispatch:  # Keep manual trigger
```

### Safety Controls

- **Rate limiting**: Maximum issues processed per run (`max_per_run`)
- **Dry-run mode**: Test without making changes
- **Manual trigger**: Review before automatic execution
- **Label gating**: Only processes labeled issues
- **Error handling**: Skips failed issues, continues with others

### Manual Trigger Examples

```bash
# Regular run (live mode)
gh workflow run crowdcode-issue-to-pr.yml

# Dry run (preview only)
gh workflow run crowdcode-issue-to-pr.yml --field dry_run=true

# Check run status
gh run list --workflow=crowdcode-issue-to-pr.yml --limit 5

# View logs
gh run view --log
```

---

## 2. Vote Counting

**File**: `.github/workflows/crowdcode-vote-counting.yml`

### Purpose

Counts votes from PatchPanel members on AI-generated PRs and updates vote tallies.

### Trigger Events

```yaml
on:
  pull_request_review:
    types: [submitted, edited, dismissed]
  issue_comment:
    types: [created]
  schedule:
    - cron: '0 * * * *'  # Hourly
  workflow_dispatch:
    inputs:
      dry_run:
        description: 'Dry run mode (no actual changes)'
        required: false
        default: 'false'
        type: boolean
```

**Triggers**:
- **PR review submitted/edited/dismissed** - Real-time vote counting
- **PR comment created** - Detect reaction changes
- **Scheduled**: Runs every hour
- **Manual**: Can be triggered anytime

### What It Does

**Step-by-step process**:

1. **Checkout repository** - Gets latest code
2. **Setup Python** - Installs Python 3.11
3. **Install dependencies** - Installs `PyGithub` and `pyyaml`
4. **Count and Update Votes** - Runs `scripts/validate-votes.py`:
   - Loads PatchPanel members from `.github/PATCHPANEL_MEMBERS.json`
   - Finds PRs labeled `crowdcode:voting`
   - For each PR:
     - Fetches all reactions (👍 👎 👀) on PR description
     - Fetches all PR reviews (APPROVED, CHANGES_REQUESTED, COMMENTED)
     - Filters votes to only PatchPanel members with `active: true`
     - Calculates vote tally:
       - Approve: 👍 reactions OR "Approved" reviews
       - Reject: 👎 reactions OR "Changes Requested" reviews
       - Review: 👀 reactions OR "Commented" reviews
     - Updates PR description with vote counts
     - Checks if quorum and threshold met
     - Updates labels accordingly:
       - Adds `crowdcode:ready-to-promote` if approved
       - Keeps `crowdcode:voting` if still pending
       - Adds `crowdcode:archived` if rejected
5. **Summary** - Generates workflow summary

### Inputs

**Manual trigger inputs**:
- `dry_run` (boolean, default: `false`) - Preview vote counts without updating

**Configuration**:
```yaml
voting:
  quorum: 3  # Minimum votes required
  approval_threshold: 0.5  # 50% approval (0.0 to 1.0)
  voting_period_days: 7
  count_reactions: true  # Count emoji reactions
  count_reviews: true    # Count PR reviews
  
  valid_reactions:
    approve: ["+1", "thumbsup", "heart"]
    reject: ["-1", "thumbsdown"]
    review: ["eyes", "thinking_face"]
  
  review_mapping:
    APPROVED: "approve"
    CHANGES_REQUESTED: "reject"
    COMMENTED: "review"
```

### Outputs

**Updated artifacts**:
- PR descriptions with vote tallies
- PR labels based on voting status
- Issue comments with vote notifications

**Workflow summary**:
- Number of PRs processed
- Vote counts updated
- PRs ready for promotion

**Vote display format** (added to PR description):
```markdown
## 🗳️ PatchPanel Vote Status

**Votes**: 5 total
- ✅ Approve: 4 (80%)
- ❌ Reject: 1 (20%)
- 👀 Review: 0

**Status**: ✅ Ready to promote (quorum met, 80% > 50% threshold)
```

### Permissions Required

```yaml
permissions:
  pull-requests: write  # Update PR descriptions and labels
  issues: write         # Post vote notifications
```

### How to Disable

**Option 1: Delete workflow file**
```bash
rm .github/workflows/crowdcode-vote-counting.yml
git add .github/workflows/crowdcode-vote-counting.yml
git commit -m "Disable CrowdCode vote counting"
git push
```

**Option 2: Disable reaction counting** (keep review counting)
Edit `.github/crowdcode-config.yml`:
```yaml
voting:
  count_reactions: false  # Disable reaction counting
  count_reviews: true     # Keep review counting
```

**Option 3: Disable automatic counting** (manual only)
Edit workflow file:
```yaml
on:
  # pull_request_review:  # Comment out
  #   types: [submitted, edited, dismissed]
  # issue_comment:  # Comment out
  #   types: [created]
  # schedule:  # Comment out
  #   - cron: '0 * * * *'
  workflow_dispatch:  # Keep manual trigger
```

### Safety Controls

- **PatchPanel gating**: Only counts votes from authorized members
- **Active status check**: Only counts votes from `active: true` members
- **Dry-run mode**: Preview vote counts without changes
- **Label filtering**: Only processes PRs labeled `crowdcode:voting`

---

## 3. Feature Promotion

**File**: `.github/workflows/crowdcode-feature-promotion.yml`

### Purpose

Merges approved features to the main branch when voting thresholds are met.

**⚠️ Critical**: This workflow modifies the main branch. Ensure proper configuration before enabling.

### Trigger Events

```yaml
on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6:00 AM UTC
  workflow_dispatch:
    inputs:
      dry_run:
        description: 'Dry run mode (no actual changes)'
        required: false
        default: 'false'
        type: boolean
```

**Triggers**:
- **Scheduled**: Runs daily at 6:00 AM UTC
- **Manual**: Can be triggered anytime

### What It Does

**Step-by-step process**:

1. **Checkout repository** - Gets full history (`fetch-depth: 0`)
2. **Setup Python** - Installs Python 3.11
3. **Install dependencies** - Installs `PyGithub` and `pyyaml`
4. **Promote Features** - Runs `scripts/promote-feature.py`:
   - Finds PRs labeled `crowdcode:ready-to-promote`
   - For each PR:
     - **Re-verify votes** (ensure threshold still met)
     - Run security checks if enabled (`require_codeql: true`)
     - Run tests if enabled (`require_tests: true`)
     - Merge to main using configured method (`merge_method`)
     - Update PR labels:
       - Remove: `crowdcode:ready-to-promote`, `crowdcode:voting`
       - Add: `crowdcode:promoted`
     - Close linked issue with success comment
     - Preserve feature branch (unless `auto_delete_branch: true`)
     - Notify PatchPanel members if enabled
     - Update changelog if enabled
5. **Summary** - Generates promotion report

### Inputs

**Manual trigger inputs**:
- `dry_run` (boolean, default: `false`) - Preview promotions without merging

**Configuration**:
```yaml
promotion:
  merge_method: "squash"  # Options: merge, squash, rebase
  require_tests: false    # Require CI tests to pass
  require_codeql: false   # Require CodeQL security scan
  auto_delete_branch: false  # Keep feature branches visible
  auto_deploy: false      # Auto-deploy after merge
  notify_members: true    # Notify PatchPanel of promotions

branches:
  base_branch: "main"  # Target branch for merges
```

### Outputs

**Modified artifacts**:
- Main branch updated with merged features
- PR closed and labeled `crowdcode:promoted`
- Feature branch preserved (if `auto_delete_branch: false`)
- Issue closed with success comment
- Changelog updated (if enabled)

**Workflow summary**:
- Number of PRs promoted
- Merge conflicts (if any)
- Test or security failures

### Permissions Required

```yaml
permissions:
  pull-requests: write  # Close PRs and update labels
  contents: write       # Merge to main branch
  issues: write         # Close linked issues
```

### How to Disable

**Option 1: Delete workflow file** (complete removal)
```bash
rm .github/workflows/crowdcode-feature-promotion.yml
git add .github/workflows/crowdcode-feature-promotion.yml
git commit -m "Disable CrowdCode feature promotion"
git push
```

**Option 2: Manual promotion only** (disable automatic)
Edit workflow file:
```yaml
on:
  # schedule:  # Comment out automatic schedule
  #   - cron: '0 6 * * *'
  workflow_dispatch:  # Keep manual trigger
```

**Option 3: Require manual approval** (add approval gate)
Edit workflow to add `environment` requirement:
```yaml
jobs:
  promote-features:
    runs-on: ubuntu-latest
    environment: production  # Requires manual approval in Settings → Environments
```

### Safety Controls

- **Vote re-verification**: Confirms threshold still met before merge
- **Test requirements**: Optional CI test gating (`require_tests: true`)
- **Security scans**: Optional CodeQL requirement (`require_codeql: true`)
- **Dry-run mode**: Preview promotions without merging
- **Branch preservation**: Feature branches kept by default
- **Manual trigger**: Review before automatic execution

### Manual Trigger Examples

```bash
# Regular promotion
gh workflow run crowdcode-feature-promotion.yml

# Dry run (preview only)
gh workflow run crowdcode-feature-promotion.yml --field dry_run=true

# Check promotion history
gh run list --workflow=crowdcode-feature-promotion.yml --limit 10
```

---

## 4. Branch Visibility

**File**: `.github/workflows/crowdcode-branch-visibility.yml`

### Purpose

Maintains a public dashboard of all feature branches, including rejected/unmerged features for transparency.

### Trigger Events

```yaml
on:
  push:
    branches:
      - 'crowdcode/feature-*'  # Any feature branch push
  pull_request:
    types: [opened, closed, reopened]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday at midnight UTC
  workflow_dispatch:
```

**Triggers**:
- **Feature branch push** - Update when branches change
- **PR state change** - Update when PRs open/close
- **Scheduled**: Runs weekly on Sunday
- **Manual**: Can be triggered anytime

### What It Does

**Step-by-step process**:

1. **Checkout repository** - Gets full history (`fetch-depth: 0`)
2. **Setup Python** - Installs Python 3.11
3. **Install dependencies** - Installs `PyGithub` and `pyyaml`
4. **Generate Feature Dashboard** - Runs `scripts/generate-dashboard.py`:
   - Lists all `crowdcode/feature-*` branches
   - For each branch:
     - Extracts issue number and slug
     - Fetches linked PR and issue
     - Gets current status (voting, promoted, archived)
     - Collects vote tallies
     - Records creation date and author
   - Generates JSON index: `docs/features/index.json`
   - Generates Markdown dashboard: `docs/features/README.md`
   - Updates main README with feature list (if enabled)
5. **Commit Dashboard Updates** - Commits changes to repository
6. **Summary** - Generates dashboard report

### Inputs

**Configuration**:
```yaml
dashboard:
  enabled: true  # Enable/disable dashboard generation
  path: "docs/features"
  update_readme: true  # Update main README
  generate_changelog: true
```

### Outputs

**Generated files**:
- `docs/features/index.json` - Machine-readable feature index
- `docs/features/README.md` - Human-readable feature dashboard
- Updated main README (if `update_readme: true`)

**JSON structure**:
```json
{
  "features": [
    {
      "branch": "crowdcode/feature-42-dark-mode",
      "issue": 42,
      "pr": 43,
      "status": "voting",
      "created": "2025-12-29T00:00:00Z",
      "votes": {
        "approve": 5,
        "reject": 1,
        "review": 2
      },
      "description": "Add dark mode support",
      "author": "username"
    }
  ],
  "updated": "2025-12-29T15:00:00Z"
}
```

### Permissions Required

```yaml
permissions:
  contents: write  # Commit dashboard updates
```

### How to Disable

**Option 1: Delete workflow file**
```bash
rm .github/workflows/crowdcode-branch-visibility.yml
git add .github/workflows/crowdcode-branch-visibility.yml
git commit -m "Disable CrowdCode branch visibility dashboard"
git push
```

**Option 2: Disable dashboard generation**
Edit `.github/crowdcode-config.yml`:
```yaml
dashboard:
  enabled: false  # Disable dashboard
```

**Option 3: Disable automatic updates** (manual only)
Edit workflow file:
```yaml
on:
  # push:  # Comment out
  #   branches:
  #     - 'crowdcode/feature-*'
  # pull_request:  # Comment out
  #   types: [opened, closed, reopened]
  # schedule:  # Comment out
  #   - cron: '0 0 * * 0'
  workflow_dispatch:  # Keep manual trigger
```

### Safety Controls

- **Read-only dashboard**: Only displays data, doesn't modify features
- **Commit gating**: Checks for changes before committing
- **Skip CI tag**: Uses `[skip ci]` in commit message to prevent loops
- **Manual trigger**: Can be run on-demand

---

## Workflow Dependencies

### Execution Order

```
1. Issue to PR (Daily 2 AM)
        ↓
2. Vote Counting (Hourly + on reactions)
        ↓
3. Feature Promotion (Daily 6 AM)
        ↓
4. Branch Visibility (Weekly + on push)
```

### Data Flow

```
Issue → PR → Votes → Promotion → Dashboard
  ↓      ↓      ↓         ↓           ↓
Labels  Code  Tally    Merge     Visibility
```

---

## Common Workflow Patterns

### Dry-Run Testing

Test any workflow without making changes:

```bash
# Test PR generation
gh workflow run crowdcode-issue-to-pr.yml --field dry_run=true

# Test vote counting
gh workflow run crowdcode-vote-counting.yml --field dry_run=true

# Test promotion
gh workflow run crowdcode-feature-promotion.yml --field dry_run=true
```

### Manual Execution

Trigger workflows manually for testing:

```bash
# List all workflows
gh workflow list

# Run specific workflow
gh workflow run crowdcode-issue-to-pr.yml

# View run status
gh run list --limit 5

# View detailed logs
gh run view --log
```

### Monitoring Workflow Runs

```bash
# List recent runs
gh run list --workflow=crowdcode-issue-to-pr.yml --limit 10

# Watch run in progress
gh run watch

# View logs for failed run
gh run view RUN_ID --log-failed
```

---

## Disabling All CrowdCode Workflows

To completely disable CrowdCode:

```bash
# Option 1: Delete all workflow files
rm .github/workflows/crowdcode-*.yml
git add .github/workflows/
git commit -m "Disable all CrowdCode workflows"
git push

# Option 2: Rename to disable (easier to re-enable)
for file in .github/workflows/crowdcode-*.yml; do
  mv "$file" "$file.disabled"
done
git add .github/workflows/
git commit -m "Temporarily disable CrowdCode"
git push

# Option 3: Disable in GitHub UI
# Settings → Actions → Disable specific workflows
```

---

## Troubleshooting

### Workflow Not Running

**Symptoms**: Scheduled workflow doesn't execute

**Causes**:
- Workflow file syntax error
- GitHub Actions disabled in repository
- Incorrect schedule syntax
- Repository inactive (GitHub pauses schedules)

**Solutions**:
```bash
# Validate YAML syntax
yamllint .github/workflows/crowdcode-*.yml

# Check Actions enabled
# Settings → Actions → General → "Allow all actions"

# Manually trigger to test
gh workflow run crowdcode-issue-to-pr.yml

# Check workflow logs
gh run list --workflow=crowdcode-issue-to-pr.yml --limit 1
```

### Permission Denied

**Symptoms**: "Resource not accessible by integration" error

**Solutions**:
- Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"
- Enable "Allow GitHub Actions to create and approve pull requests"

### Workflow Timeout

**Symptoms**: Workflow runs but times out

**Solutions**:
- Reduce `max_per_run` in config
- Increase `timeout_seconds` in config
- Check for rate limiting
- Review logs for bottlenecks

---

## Security Considerations

### Permissions Audit

Review permissions granted to workflows:

```yaml
# Minimal permissions principle
permissions:
  contents: write        # Only if merging/committing
  issues: write          # Only if updating issues
  pull-requests: write   # Only if updating PRs
```

**Recommendation**: Grant only necessary permissions per workflow.

### Secrets Handling

**Never** log or expose secrets:

```yaml
# Bad - logs secret
- run: echo ${{ secrets.API_KEY }}

# Good - uses secret safely
- run: python script.py
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

### Third-Party Actions

CrowdCode uses only official GitHub actions:
- `actions/checkout@v4` - Official GitHub action
- `actions/setup-python@v4` - Official GitHub action

**Recommendation**: Review any third-party actions before use.

---

## Next Steps

1. ✅ Understand workflow automation
2. 📖 Read [Governance Guide](governance.md) for voting configuration
3. 🛡️ Read [Threat Model](threat-model.md) for security
4. ⚙️ Configure workflows in your repository

---

**Need help?** See [Setup Guide](setup.md) or [Documentation Index](index.md).
