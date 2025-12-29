# CrowdCode Setup Guide

> **Install CrowdCode safely in your repository**

This guide walks you through installing and configuring CrowdCode in a repository, with emphasis on safe trial and control mechanisms.

## Prerequisites

- GitHub repository with admin access
- GitHub Actions enabled
- Python 3.11+ (for workflow scripts)
- Familiarity with GitHub Issues, Pull Requests, and Actions

## Quick Trial

**⚠️ Recommended**: Try CrowdCode in a test repository first before production use.

```bash
# Create a test repository
gh repo create my-org/crowdcode-trial --public --clone

# Follow installation steps below in test repo
# Experiment with feature requests and voting
# Verify behavior meets your needs
# Then deploy to production repository
```

## Installation Steps

### 1. Copy CrowdCode Files

Clone or download the CrowdCode repository and copy files to your target repository:

```bash
# Clone CrowdCode (if not already cloned)
git clone https://github.com/gitbrainlab/CrowdCode.git
cd CrowdCode

# Navigate to your target repository
cd /path/to/your-repo

# Create required directories
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p scripts
mkdir -p docs/features

# Copy workflow files
cp /path/to/CrowdCode/.github/workflows/crowdcode-*.yml .github/workflows/

# Copy configuration files
cp /path/to/CrowdCode/.github/PATCHPANEL_MEMBERS.json .github/
cp /path/to/CrowdCode/.github/crowdcode-config.yml .github/
cp /path/to/CrowdCode/.github/ISSUE_TEMPLATE/feature-request.yml .github/ISSUE_TEMPLATE/

# Copy scripts
cp /path/to/CrowdCode/scripts/*.py scripts/

# Make scripts executable
chmod +x scripts/*.py
```

**Files copied:**
- 4 workflow files (`.github/workflows/crowdcode-*.yml`)
- 1 configuration file (`.github/crowdcode-config.yml`)
- 1 membership file (`.github/PATCHPANEL_MEMBERS.json`)
- 1 issue template (`.github/ISSUE_TEMPLATE/feature-request.yml`)
- 4 Python scripts (`scripts/*.py`)

### 2. Configure PatchPanel Membership

Edit `.github/PATCHPANEL_MEMBERS.json` to define initial voters:

```json
{
  "version": "1.0",
  "updated": "2025-12-29T00:00:00Z",
  "description": "Authorized PatchPanel members for CrowdCode voting",
  "members": [
    {
      "github_username": "your-github-username",
      "joined": "2025-12-29T00:00:00Z",
      "role": "founding",
      "active": true,
      "notes": "Project maintainer"
    },
    {
      "github_username": "trusted-collaborator",
      "joined": "2025-12-29T00:00:00Z",
      "role": "contributor",
      "active": true,
      "notes": "Core contributor"
    }
  ],
  "codes": {
    "prefix": "PATCH",
    "year": 2025,
    "next_sequence": 1,
    "redemption_enabled": false
  }
}
```

**Key fields:**
- `github_username`: Exact GitHub username (case-sensitive)
- `active`: Must be `true` for votes to count
- `role`: "founding", "contributor", "community", or "emeritus"

**⚠️ Security**: Keep this list small initially. Only trusted members should vote.

### 3. Create Required Labels

Create GitHub labels for CrowdCode workflow states:

```bash
# Using GitHub CLI (recommended)
gh label create "crowdcode:feature-request" \
  --color "0e8a16" \
  --description "New feature idea submitted by community"

gh label create "crowdcode:pending-pr" \
  --color "fbca04" \
  --description "PR generation in progress"

gh label create "crowdcode:ai-generated" \
  --color "0075ca" \
  --description "Code created by AI (requires review)"

gh label create "crowdcode:voting" \
  --color "d93f0b" \
  --description "Active voting period for PatchPanel"

gh label create "crowdcode:ready-to-promote" \
  --color "0e8a16" \
  --description "Approved by PatchPanel, ready to merge"

gh label create "crowdcode:promoted" \
  --color "6f42c1" \
  --description "Successfully merged to main branch"

gh label create "crowdcode:archived" \
  --color "d4c5f9" \
  --description "Rejected or superseded feature"
```

**Manual creation** (if `gh` CLI not available):
1. Go to repository → Settings → Labels
2. Click "New label"
3. Enter name, color, and description from above
4. Repeat for all 7 labels

**⚠️ Important**: Label names must match exactly (case-sensitive).

### 4. Configure Repository Permissions

Grant GitHub Actions necessary permissions:

1. Go to repository → Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select **"Read and write permissions"**
4. Check ✅ **"Allow GitHub Actions to create and approve pull requests"**
5. Click "Save"

**Permissions required:**
- `contents: write` - Create branches and commits
- `issues: write` - Update issue labels and comments
- `pull-requests: write` - Create and update PRs

**⚠️ Security**: These permissions allow workflows to modify repository. Review workflow code before enabling.

### 5. Set Up Required Secrets (Optional)

CrowdCode uses GitHub's built-in `GITHUB_TOKEN` by default. Additional secrets are optional:

**Optional secrets** (for future AI integration):
```bash
# If using OpenAI API for code generation
gh secret set OPENAI_API_KEY --body "sk-..."

# If using GitHub Copilot API
gh secret set COPILOT_API_KEY --body "ghu_..."
```

**Notification webhooks** (optional):
```bash
gh secret set SLACK_WEBHOOK --body "https://hooks.slack.com/..."
gh secret set DISCORD_WEBHOOK --body "https://discord.com/api/webhooks/..."
```

**⚠️ Privacy**: Secrets are encrypted but accessible to workflows. Only add trusted secrets.

### 6. Configure Workflow Schedules

Review and adjust workflow schedules in `.github/crowdcode-config.yml`:

```yaml
# Issue Processing
issue_processing:
  max_per_run: 5  # Limit to prevent spam (increase gradually)

# Voting System
voting:
  quorum: 3  # Minimum votes required
  approval_threshold: 0.5  # 50% approval (0.0 to 1.0)
  voting_period_days: 7  # Voting window

# Feature Promotion
promotion:
  merge_method: "squash"  # Options: merge, squash, rebase
  require_tests: false  # Require passing CI tests
  require_codeql: false  # Require security scan
  auto_delete_branch: false  # Keep branches visible
```

**Recommended initial settings:**
- Small team (2-5 people): `quorum: 2`, `approval_threshold: 0.5`
- Medium team (6-20): `quorum: 3`, `approval_threshold: 0.5`
- Large team (20+): `quorum: 5`, `approval_threshold: 0.6`

**Schedule adjustments** (edit workflow files if needed):
- `crowdcode-issue-to-pr.yml`: Daily at 2 AM UTC (`cron: '0 2 * * *'`)
- `crowdcode-vote-counting.yml`: Hourly (`cron: '0 * * * *'`)
- `crowdcode-feature-promotion.yml`: Daily at 6 AM UTC (`cron: '0 6 * * *'`)
- `crowdcode-branch-visibility.yml`: Weekly on Sunday (`cron: '0 0 * * 0'`)

### 7. Initialize Python Dependencies

Add Python dependencies to your repository (if not using Docker):

Create `requirements.txt`:
```txt
PyGithub>=2.1.1
pyyaml>=6.0
```

**For workflows**, dependencies are installed automatically:
```yaml
# Already in workflow files
- name: Install dependencies
  run: |
    pip install PyGithub pyyaml
```

### 8. Test the Installation

#### Test 1: Verify Workflow Files

```bash
# Check workflows are recognized
gh workflow list | grep crowdcode

# Should show:
# CrowdCode - Issue to PR
# CrowdCode - Vote Counting
# CrowdCode - Feature Promotion
# CrowdCode - Branch Visibility
```

#### Test 2: Create Test Feature Request

```bash
# Create test issue
gh issue create \
  --title "[FEATURE] Test CrowdCode Installation" \
  --label "crowdcode:feature-request" \
  --body "This is a test feature to verify CrowdCode is working correctly."

# Or use web interface:
# Go to Issues → New Issue → Select "CrowdCode Feature Request" template
```

#### Test 3: Manually Trigger Workflows

```bash
# Trigger PR generation (dry run mode for safety)
gh workflow run crowdcode-issue-to-pr.yml --field dry_run=true

# Check run status
gh run list --workflow=crowdcode-issue-to-pr.yml --limit 1

# View run logs
gh run view --log
```

#### Test 4: Verify Labels Applied

After workflow runs:
```bash
# List issues with CrowdCode labels
gh issue list --label "crowdcode:feature-request"
gh issue list --label "crowdcode:pending-pr"
```

### 9. Configure Branch Protection (Recommended)

Protect main branch to prevent accidental direct pushes:

```bash
# Protect main branch
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks[strict]=true \
  --field required_status_checks[contexts][]=[] \
  --field enforce_admins=false \
  --field required_pull_request_reviews=null \
  --field restrictions=null
```

**Or manually:**
1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable: "Require pull request before merging"
4. Optional: "Require status checks to pass"
5. **Do NOT** enable "Require review" (voting replaces this)

**⚠️ Critical**: Do NOT block GitHub Actions from pushing to main, as promotion workflow needs write access.

### 10. Update Repository README

Add CrowdCode badge and links to your README.md:

```markdown
# Your Project

[![CrowdCode Enabled](https://img.shields.io/badge/CrowdCode-Enabled-brightgreen)](./docs/index.md)

## Community Features

This project uses [CrowdCode](./docs/index.md) for collaborative feature development.

- 💡 [Submit a feature idea](../../issues/new?template=feature-request.yml)
- 🗳️ [Vote on features](../../pulls?q=is%3Apr+label%3Acrowdcode%3Avoting)
- 🌿 [Browse all feature branches](../../branches/all?query=crowdcode%2Ffeature)
- 📖 [Learn about CrowdCode](./docs/index.md)
```

## Configuration Reference

### File: `.github/crowdcode-config.yml`

Complete configuration with explanations:

```yaml
# CrowdCode Platform Configuration

# Issue Processing
issue_processing:
  max_per_run: 5  # Safety: Limit issues processed per workflow run
  labels:
    feature_request: "crowdcode:feature-request"
    pending_pr: "crowdcode:pending-pr"
    ai_generated: "crowdcode:ai-generated"
    voting: "crowdcode:voting"
    ready_to_promote: "crowdcode:ready-to-promote"
    promoted: "crowdcode:promoted"
    archived: "crowdcode:archived"

# AI Code Generation (Phase 2 - Not yet active)
ai_generation:
  enabled: false  # OFF SWITCH: Disable AI generation
  model: "gpt-4"
  max_tokens: 4000
  temperature: 0.7
  retry_attempts: 3
  timeout_seconds: 300

# Voting System
voting:
  quorum: 3  # Minimum votes required
  approval_threshold: 0.5  # 50% approval (0.0 to 1.0)
  voting_period_days: 7
  auto_close_on_threshold: true
  count_reactions: true  # Count 👍 👎 👀 reactions
  count_reviews: true  # Count PR reviews
  
  valid_reactions:
    approve: ["+1", "thumbsup", "heart"]
    reject: ["-1", "thumbsdown"]
    review: ["eyes", "thinking_face"]
  
  review_mapping:
    APPROVED: "approve"
    CHANGES_REQUESTED: "reject"
    COMMENTED: "review"

# Feature Promotion
promotion:
  merge_method: "squash"  # Options: merge, squash, rebase
  require_tests: false  # OFF SWITCH: Require CI tests
  require_codeql: false  # OFF SWITCH: Require security scan
  auto_delete_branch: false  # Keep branches visible
  auto_deploy: false  # OFF SWITCH: Auto-deploy after merge
  notify_members: true

# Branch Management
branches:
  prefix: "crowdcode/feature"
  base_branch: "main"
  protection_rules:
    require_review: false  # Voting replaces traditional review
    require_status_checks: false

# PatchPanel
patchpanel:
  membership_file: ".github/PATCHPANEL_MEMBERS.json"
  allow_membership_requests: true
  require_physical_codes: false
  membership_issue_label: "crowdcode:membership-request"

# Notifications
notifications:
  slack:
    enabled: false  # OFF SWITCH: Slack notifications
    webhook_secret: "SLACK_WEBHOOK"
  discord:
    enabled: false  # OFF SWITCH: Discord notifications
    webhook_secret: "DISCORD_WEBHOOK"
  github:
    enabled: true
    mention_on_promotion: true

# Dashboard
dashboard:
  enabled: true  # OFF SWITCH: Feature dashboard
  path: "docs/features"
  update_readme: true
  generate_changelog: true
```

### File: `.github/PATCHPANEL_MEMBERS.json`

```json
{
  "version": "1.0",
  "updated": "2025-12-29T00:00:00Z",
  "description": "Authorized PatchPanel members for CrowdCode voting",
  "members": [
    {
      "github_username": "username",  // Exact GitHub username
      "joined": "2025-12-29T00:00:00Z",  // ISO 8601 timestamp
      "role": "founding",  // founding|contributor|community|emeritus
      "active": true,  // Must be true for votes to count
      "notes": "Optional description"
    }
  ],
  "codes": {
    "prefix": "PATCH",  // Physical code prefix
    "year": 2025,
    "next_sequence": 1,  // Next code number
    "redemption_enabled": false  // OFF SWITCH: Code redemption
  }
}
```

## Verification Checklist

After installation, verify:

- [ ] All 4 workflow files in `.github/workflows/`
- [ ] Configuration file `.github/crowdcode-config.yml` exists
- [ ] Membership file `.github/PATCHPANEL_MEMBERS.json` has valid members
- [ ] All 7 labels created in repository
- [ ] GitHub Actions has "Read and write permissions"
- [ ] Test issue created with `crowdcode:feature-request` label
- [ ] Dry-run workflow executed successfully
- [ ] Branch protection on `main` (recommended)
- [ ] README updated with CrowdCode information

## Troubleshooting

### Workflows Not Appearing

**Problem**: Workflows don't show in Actions tab

**Solutions**:
- Ensure files are in `.github/workflows/` directory
- Check YAML syntax is valid: `yamllint .github/workflows/*.yml`
- Commit and push workflow files to default branch
- Refresh Actions tab in GitHub

### Permission Errors

**Problem**: Workflow fails with "Resource not accessible by integration"

**Solutions**:
- Verify "Read and write permissions" enabled in Settings → Actions
- Check "Allow GitHub Actions to create and approve pull requests" is checked
- Ensure `GITHUB_TOKEN` has correct scopes in workflow files

### Labels Not Working

**Problem**: Issues/PRs not getting labeled

**Solutions**:
- Verify label names match exactly (case-sensitive)
- Check labels exist: `gh label list`
- Review workflow logs for label creation errors
- Manually create missing labels

### PatchPanel Votes Not Counting

**Problem**: Reactions or reviews don't affect vote count

**Solutions**:
- Verify username spelling in `PATCHPANEL_MEMBERS.json` (case-sensitive)
- Ensure `active: true` for the member
- Check PR has `crowdcode:voting` label
- Wait for hourly vote counting workflow to run
- Manually trigger: `gh workflow run crowdcode-vote-counting.yml`

### Too Many Issues Processed

**Problem**: Workflow processes more issues than desired

**Solutions**:
- Reduce `issue_processing.max_per_run` in config
- Disable workflow temporarily
- Remove `crowdcode:feature-request` label from issues

## Security Checklist

Before enabling in production:

- [ ] Review all workflow code for security issues
- [ ] Limit PatchPanel to trusted members only
- [ ] Enable branch protection on main branch
- [ ] Set reasonable `max_per_run` limit (start with 1-2)
- [ ] Disable AI generation until needed (`ai_generation.enabled: false`)
- [ ] Review data sent to external APIs (if any)
- [ ] Test in isolated repository first
- [ ] Monitor workflow runs for suspicious activity
- [ ] Have rollback plan ready (disable workflows)

## Next Steps

1. ✅ Installation complete
2. 📖 Read [Workflows Guide](workflows.md) to understand automation
3. 🗳️ Read [Governance Guide](governance.md) to configure voting
4. 🛡️ Read [Threat Model](threat-model.md) for security considerations
5. 🚀 Create your first feature request and test the workflow!

---

**Need help?** See [Documentation Index](index.md) or [open an issue](https://github.com/gitbrainlab/CrowdCode/issues).
