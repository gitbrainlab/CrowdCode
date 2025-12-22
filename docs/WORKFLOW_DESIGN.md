# CrowdCode GitHub Actions Workflow Design

## Overview

This document describes the GitHub Actions workflows that power the CrowdCode platform, enabling automated PR generation, vote counting, and feature promotion.

## Workflow Architecture

### 1. Issue to PR Generation Workflow

**File**: `.github/workflows/issue-to-pr.yml`

**Trigger**: 
- Scheduled (daily at 2:00 AM UTC)
- Manual dispatch (workflow_dispatch)

**Purpose**: Scan for new feature request issues and generate AI-powered pull requests.

**Steps**:
1. Checkout repository
2. Find issues labeled `crowdcode:feature-request` without `crowdcode:pending-pr`
3. For each issue:
   - Parse issue content
   - Generate feature branch name
   - Use GitHub Copilot to generate code
   - Create branch and commit
   - Open pull request
   - Update issue labels
   - Link PR to issue

**Permissions Required**:
- `issues: write` - Update issue labels
- `pull-requests: write` - Create PRs
- `contents: write` - Create branches and commits

**Configuration Options**:
```yaml
env:
  MAX_ISSUES_PER_RUN: 5  # Limit PRs generated per run
  AI_MODEL: "gpt-4"       # Which AI model to use
  BRANCH_PREFIX: "crowdcode/feature"
  LABEL_FEATURE_REQUEST: "crowdcode:feature-request"
  LABEL_PENDING_PR: "crowdcode:pending-pr"
```

**Error Handling**:
- Skip issues that fail generation
- Log errors to issue comments
- Continue with next issue
- Summary report at end

### 2. Vote Counting Workflow

**File**: `.github/workflows/vote-counting.yml`

**Trigger**:
- PR review submitted
- PR reaction added
- Scheduled (hourly)
- Manual dispatch

**Purpose**: Count votes from PatchPanel members on AI-generated PRs.

**Steps**:
1. Checkout repository
2. Load PatchPanel member list
3. Find PRs labeled `crowdcode:voting`
4. For each PR:
   - Fetch all reviews and reactions
   - Filter votes from PatchPanel members only
   - Calculate vote tally (approve, reject, review needed)
   - Update PR description with vote count
   - Check if promotion threshold met
   - Update labels accordingly

**Vote Counting Logic**:
```yaml
Votes:
  Approve: 👍 reaction OR "Approve" review
  Reject: 👎 reaction OR "Request changes" review
  Review: 👀 reaction OR "Comment" review

Valid Vote: Author in PATCHPANEL_MEMBERS.json

Promotion Criteria:
  - Minimum quorum (default: 3 votes)
  - Majority approval (>50% approve)
  - No blocking issues
```

**Output**:
- Updated PR description with vote summary
- Labels updated based on voting status
- Issue comment with vote notification

### 3. Feature Promotion Workflow

**File**: `.github/workflows/feature-promotion.yml`

**Trigger**:
- Scheduled (daily at 6:00 AM UTC)
- Label added: `crowdcode:ready-to-promote`
- Manual dispatch

**Purpose**: Merge approved features to main branch.

**Steps**:
1. Checkout repository
2. Find PRs labeled `crowdcode:ready-to-promote`
3. For each PR:
   - Verify vote threshold still met
   - Run security checks (CodeQL)
   - Run tests (if configured)
   - Merge to main (or rebase)
   - Update labels to `crowdcode:promoted`
   - Close linked issue with success comment
   - Notify PatchPanel members

**Merge Strategy**:
```yaml
# Configurable in crowdcode-config.yml
merge_method: "squash"  # Options: merge, squash, rebase
require_tests: true
require_codeql: true
auto_delete_branch: false  # Keep feature branches visible
```

**Post-Merge Actions**:
- Tag release (optional)
- Deploy (if configured)
- Generate changelog entry
- Update feature dashboard

### 4. Branch Visibility Workflow

**File**: `.github/workflows/branch-visibility.yml`

**Trigger**:
- Push to feature branch
- PR opened/closed
- Scheduled (weekly)

**Purpose**: Maintain a public index of all feature branches, even those not merged.

**Steps**:
1. List all `crowdcode/feature-*` branches
2. Generate branch index JSON
3. Build feature dashboard (GitHub Pages)
4. Publish to `docs/features/index.json`
5. Update README with feature list

**Dashboard Data Structure**:
```json
{
  "features": [
    {
      "branch": "crowdcode/feature-42-dark-mode",
      "issue": 42,
      "pr": 43,
      "status": "voting",
      "created": "2025-12-21T00:00:00Z",
      "votes": {
        "approve": 5,
        "reject": 1,
        "review": 2
      },
      "description": "Add dark mode support"
    }
  ],
  "updated": "2025-12-21T21:00:00Z"
}
```

### 5. PatchPanel Management Workflow

**File**: `.github/workflows/patchpanel-management.yml`

**Trigger**:
- Issue labeled `crowdcode:membership-request`
- Manual dispatch

**Purpose**: Manage PatchPanel membership requests.

**Steps**:
1. Validate membership request format
2. Check physical code (if provided)
3. Verify requester identity
4. Update PATCHPANEL_MEMBERS.json
5. Commit and push changes
6. Notify requester
7. Close membership issue

**Membership Request Format**:
```yaml
---
type: membership-request
github_username: octocat
physical_code: PATCH-2025-ABCD  # Optional
reason: "Active contributor since..."
---
```

## Workflow Dependencies

```
issue-to-pr.yml
    ↓
vote-counting.yml
    ↓
feature-promotion.yml
    ↓
branch-visibility.yml
```

## Environment Variables & Secrets

### Required Secrets
- `GITHUB_TOKEN` - Built-in, automatic
- `COPILOT_API_KEY` - GitHub Copilot API access (future)

### Optional Secrets
- `SLACK_WEBHOOK` - Notifications
- `DISCORD_WEBHOOK` - Notifications
- `ANALYTICS_TOKEN` - Usage tracking

### Configuration Files
- `.github/PATCHPANEL_MEMBERS.json` - Voter list
- `.github/crowdcode-config.yml` - Platform settings

## Workflow Configuration File

**File**: `.github/crowdcode-config.yml`

```yaml
# CrowdCode Platform Configuration

# Issue Processing
issue_processing:
  max_per_run: 5
  labels:
    feature_request: "crowdcode:feature-request"
    pending_pr: "crowdcode:pending-pr"
    ai_generated: "crowdcode:ai-generated"
    voting: "crowdcode:voting"
    promoted: "crowdcode:promoted"
    archived: "crowdcode:archived"

# AI Code Generation
ai_generation:
  model: "gpt-4"
  max_tokens: 4000
  temperature: 0.7
  retry_attempts: 3
  timeout_seconds: 300

# Voting System
voting:
  quorum: 3                    # Minimum votes required
  approval_threshold: 0.5      # 50% approval needed
  voting_period_days: 7        # How long voting stays open
  auto_close_on_threshold: true
  count_reactions: true
  count_reviews: true
  valid_reactions:
    approve: ["+1", "thumbsup"]
    reject: ["-1", "thumbsdown"]
    review: ["eyes"]

# Feature Promotion
promotion:
  merge_method: "squash"       # merge, squash, or rebase
  require_tests: true
  require_codeql: true
  auto_delete_branch: false    # Keep branches visible
  auto_deploy: false
  notify_members: true

# Branch Management
branches:
  prefix: "crowdcode/feature"
  base_branch: "main"
  protection_rules:
    require_review: false      # AI generates, humans vote
    require_status_checks: true

# PatchPanel
patchpanel:
  membership_file: ".github/PATCHPANEL_MEMBERS.json"
  allow_membership_requests: true
  require_physical_codes: false
  membership_issue_label: "crowdcode:membership-request"

# Notifications
notifications:
  slack:
    enabled: false
    webhook_secret: "SLACK_WEBHOOK"
  discord:
    enabled: false
    webhook_secret: "DISCORD_WEBHOOK"
  github:
    enabled: true
    mention_on_promotion: true

# Dashboard
dashboard:
  enabled: true
  path: "docs/features"
  update_readme: true
  generate_changelog: true
```

## Sample Workflow Files

### Minimal Issue-to-PR Workflow

```yaml
name: CrowdCode - Issue to PR

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:

jobs:
  generate-prs:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install PyGithub openai pyyaml
      
      - name: Generate PRs from Issues
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/generate-feature-pr.py
```

### Minimal Vote Counting Workflow

```yaml
name: CrowdCode - Vote Counting

on:
  pull_request_review:
    types: [submitted]
  issue_comment:
    types: [created]
  schedule:
    - cron: '0 * * * *'  # Hourly
  workflow_dispatch:

jobs:
  count-votes:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      issues: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Count and Update Votes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/validate-votes.py
```

## Testing Workflows

### Dry-Run Mode
All workflows support a dry-run mode that simulates actions without making changes:

```bash
# Test PR generation
gh workflow run issue-to-pr.yml -f dry_run=true

# Test vote counting
gh workflow run vote-counting.yml -f dry_run=true

# Test promotion
gh workflow run feature-promotion.yml -f dry_run=true
```

### Local Testing
```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act -j generate-prs -s GITHUB_TOKEN=your_token
```

## Monitoring & Observability

### Workflow Metrics
- PR generation success rate
- Vote participation rate
- Time to promotion
- Feature adoption rate

### Logs
- All workflows log to Actions console
- Error notifications to issue comments
- Summary reports in PRs

### Alerts
- Failed PR generation
- Stalled votes
- Security vulnerabilities in AI code

## Best Practices

1. **Start Simple**: Use manual triggers initially
2. **Test Thoroughly**: Use dry-run mode before automation
3. **Monitor Activity**: Check workflow runs regularly
4. **Iterate Quickly**: Adjust thresholds based on community size
5. **Document Changes**: Update config in version control
6. **Secure Secrets**: Use GitHub encrypted secrets
7. **Limit Rate**: Don't overwhelm with too many PRs
8. **Review AI Output**: Human oversight is critical

## Troubleshooting

### Common Issues

**PR generation fails**
- Check GITHUB_TOKEN permissions
- Verify issue format matches template
- Check API rate limits

**Votes not counting**
- Verify username in PATCHPANEL_MEMBERS.json
- Check reaction/review format
- Ensure label `crowdcode:voting` is present

**Promotion blocked**
- Review security scan results
- Check test failures
- Verify quorum met

**Branch not visible**
- Run branch-visibility workflow manually
- Check GitHub Pages deployment
- Verify branch naming convention

## Future Enhancements

- **Advanced AI**: Multi-model consensus
- **Smart Scheduling**: Priority-based queue
- **Conflict Resolution**: Auto-merge conflict detection
- **A/B Testing**: Deploy features to subsets
- **Analytics Dashboard**: Real-time metrics
- **Mobile App**: Vote on mobile
- **Integration API**: Third-party tools
