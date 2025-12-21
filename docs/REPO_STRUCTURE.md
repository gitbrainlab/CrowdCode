# CrowdCode Repository Structure

## Overview

This document describes the recommended repository structure for projects using the CrowdCode platform. The structure is designed to be minimal, portable, and adaptable to any GitHub repository.

## Minimal CrowdCode Setup

### Required Files

```
your-repo/
├── .github/
│   ├── workflows/
│   │   ├── crowdcode-issue-to-pr.yml      # Generate PRs from issues
│   │   ├── crowdcode-vote-counting.yml    # Count PatchPanel votes
│   │   └── crowdcode-feature-promotion.yml # Promote approved features
│   ├── ISSUE_TEMPLATE/
│   │   └── feature-request.yml             # Structured feature template
│   ├── PATCHPANEL_MEMBERS.json             # Authorized voters
│   └── crowdcode-config.yml                # Platform configuration
├── scripts/
│   ├── generate-feature-pr.py              # AI-powered PR generation
│   ├── validate-votes.py                   # Vote counting logic
│   └── promote-feature.py                  # Feature promotion script
├── docs/
│   └── features/                           # Feature tracking (optional)
│       ├── index.json                      # Feature dashboard data
│       └── README.md                       # Feature list
├── CROWDCODE.md                            # Platform documentation
└── README.md                               # Include CrowdCode badge/info
```

## File Descriptions

### `.github/workflows/crowdcode-issue-to-pr.yml`

**Purpose**: Automated PR generation from feature request issues

**Minimal Example**:
```yaml
name: CrowdCode - Issue to PR

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:

permissions:
  issues: write
  pull-requests: write
  contents: write

jobs:
  generate-prs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install PyGithub openai pyyaml
      
      - name: Generate PRs from Issues
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/generate-feature-pr.py
```

### `.github/workflows/crowdcode-vote-counting.yml`

**Purpose**: Count votes from PatchPanel members

**Minimal Example**:
```yaml
name: CrowdCode - Vote Counting

on:
  pull_request_review:
  issue_comment:
  schedule:
    - cron: '0 * * * *'  # Hourly
  workflow_dispatch:

permissions:
  pull-requests: write
  issues: write

jobs:
  count-votes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install PyGithub pyyaml
      
      - name: Count Votes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/validate-votes.py
```

### `.github/workflows/crowdcode-feature-promotion.yml`

**Purpose**: Merge approved features to main

**Minimal Example**:
```yaml
name: CrowdCode - Feature Promotion

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:

permissions:
  pull-requests: write
  contents: write
  issues: write

jobs:
  promote-features:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for merging
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install PyGithub pyyaml
      
      - name: Promote Features
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/promote-feature.py
```

### `.github/ISSUE_TEMPLATE/feature-request.yml`

**Purpose**: Structured template for feature requests

```yaml
name: CrowdCode Feature Request
description: Submit a feature idea for AI-powered implementation
title: "[FEATURE] "
labels: ["crowdcode:feature-request"]
body:
  - type: markdown
    attributes:
      value: |
        ## CrowdCode Feature Request
        
        This feature will be reviewed and potentially implemented by AI (GitHub Copilot).
        PatchPanel members will vote on whether to promote it to the main branch.
  
  - type: input
    id: feature-name
    attributes:
      label: Feature Name
      description: Short, descriptive name for this feature
      placeholder: "e.g., Dark Mode Support"
    validations:
      required: true
  
  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: Detailed description of what this feature should do
      placeholder: |
        Describe the feature in detail:
        - What functionality should it add?
        - How should it work?
        - What should the user experience be?
    validations:
      required: true
  
  - type: textarea
    id: use-case
    attributes:
      label: Use Case / Motivation
      description: Why is this feature needed?
      placeholder: |
        Explain why this feature would be valuable:
        - What problem does it solve?
        - Who would benefit?
        - How does it align with project goals?
    validations:
      required: true
  
  - type: textarea
    id: acceptance-criteria
    attributes:
      label: Acceptance Criteria
      description: How will we know this feature is complete?
      placeholder: |
        List specific, testable criteria:
        - [ ] Criterion 1
        - [ ] Criterion 2
        - [ ] Criterion 3
    validations:
      required: false
  
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: How important is this feature?
      options:
        - Low - Nice to have
        - Medium - Would improve the project
        - High - Important for project goals
        - Critical - Blocks other work
    validations:
      required: false
  
  - type: textarea
    id: technical-notes
    attributes:
      label: Technical Notes
      description: Any technical considerations or suggestions
      placeholder: |
        Optional technical guidance for AI implementation:
        - Suggested approach
        - Files that may need changes
        - Dependencies to consider
        - Potential challenges
    validations:
      required: false
  
  - type: checkboxes
    id: terms
    attributes:
      label: CrowdCode Terms
      description: By submitting this issue, you agree that
      options:
        - label: This feature will be implemented by AI (GitHub Copilot)
          required: true
        - label: The implementation will be subject to PatchPanel voting
          required: true
        - label: The feature branch will remain public even if not merged
          required: true
```

### `.github/PATCHPANEL_MEMBERS.json`

**Purpose**: List of authorized voters

```json
{
  "version": "1.0",
  "updated": "2025-12-21T21:00:00Z",
  "description": "Authorized PatchPanel members for CrowdCode voting",
  "members": [
    {
      "github_username": "founder",
      "joined": "2025-01-01T00:00:00Z",
      "role": "founding",
      "active": true,
      "notes": "Project founder"
    },
    {
      "github_username": "contributor1",
      "joined": "2025-02-15T00:00:00Z",
      "role": "contributor",
      "active": true,
      "notes": "Active contributor"
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

### `.github/crowdcode-config.yml`

**Purpose**: Platform configuration

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
    ready_to_promote: "crowdcode:ready-to-promote"
    promoted: "crowdcode:promoted"
    archived: "crowdcode:archived"

# Voting System
voting:
  quorum: 3
  approval_threshold: 0.5
  voting_period_days: 7
  auto_close_on_threshold: true
  count_reactions: true
  count_reviews: true

# Feature Promotion
promotion:
  merge_method: "squash"
  require_tests: true
  require_codeql: false
  auto_delete_branch: false
  notify_members: true

# Branch Management
branches:
  prefix: "crowdcode/feature"
  base_branch: "main"

# PatchPanel
patchpanel:
  membership_file: ".github/PATCHPANEL_MEMBERS.json"
  allow_membership_requests: true
  require_physical_codes: false
```

### `scripts/generate-feature-pr.py`

**Purpose**: Generate PRs from feature request issues

See [Scripts Reference](#scripts-reference) below for full implementation.

### `scripts/validate-votes.py`

**Purpose**: Count and validate votes from PatchPanel members

See [Scripts Reference](#scripts-reference) below for full implementation.

### `scripts/promote-feature.py`

**Purpose**: Promote approved features to main branch

See [Scripts Reference](#scripts-reference) below for full implementation.

## Optional Enhancements

### Feature Dashboard

**Location**: `docs/features/`

**Purpose**: Public-facing dashboard of all features

**Structure**:
```
docs/features/
├── index.html          # Dashboard UI
├── index.json          # Feature data
├── style.css           # Styling
└── README.md           # Feature list (Markdown)
```

**Sample `index.json`**:
```json
{
  "generated": "2025-12-21T21:00:00Z",
  "repository": "evcatalyst/CrowdCode",
  "features": [
    {
      "id": 42,
      "name": "Dark Mode Support",
      "branch": "crowdcode/feature-42-dark-mode",
      "issue": 42,
      "pr": 43,
      "status": "voting",
      "created": "2025-12-15T00:00:00Z",
      "votes": {
        "approve": 5,
        "reject": 1,
        "review": 2,
        "total": 8
      },
      "description": "Add dark mode toggle to all interfaces"
    }
  ],
  "statistics": {
    "total_features": 10,
    "promoted": 7,
    "voting": 2,
    "pending": 1,
    "archived": 0
  }
}
```

### GitHub Pages Site

**Purpose**: Host feature dashboard and documentation

**Configuration** (in repository settings):
1. Enable GitHub Pages
2. Source: `docs/` directory
3. Custom domain (optional)

**Access**: `https://username.github.io/repo-name/features/`

### Labels

**CrowdCode Labels** (create in repository settings):

| Label | Color | Description |
|-------|-------|-------------|
| `crowdcode:feature-request` | `#0e8a16` | New feature idea |
| `crowdcode:pending-pr` | `#fbca04` | PR generation in progress |
| `crowdcode:ai-generated` | `#0075ca` | Created by AI |
| `crowdcode:voting` | `#d93f0b` | Active voting period |
| `crowdcode:ready-to-promote` | `#0e8a16` | Approved, ready to merge |
| `crowdcode:promoted` | `#6f42c1` | Merged to main |
| `crowdcode:archived` | `#d4c5f9` | Rejected or superseded |

### Branch Protection

**Recommended Settings for `main`**:
- ✅ Require pull request reviews (optional)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ❌ Do not require CrowdCode PR approval (handled by voting)

**Feature Branches**:
- No protection rules needed
- Allow force push (for AI iteration)
- Auto-delete disabled (keep for visibility)

## Integration with Existing Projects

### Adding CrowdCode to Existing Repository

**Step 1**: Install Configuration
```bash
# Create directory structure
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p scripts
mkdir -p docs/features

# Copy CrowdCode files (see above)
# - Workflows
# - Issue template
# - Config files
# - Scripts
```

**Step 2**: Initialize PatchPanel
```json
{
  "version": "1.0",
  "updated": "2025-12-21T21:00:00Z",
  "members": [
    {
      "github_username": "your-username",
      "joined": "2025-12-21T21:00:00Z",
      "role": "founding",
      "active": true
    }
  ]
}
```

**Step 3**: Create Labels
```bash
# Using GitHub CLI
gh label create "crowdcode:feature-request" --color "0e8a16"
gh label create "crowdcode:pending-pr" --color "fbca04"
gh label create "crowdcode:ai-generated" --color "0075ca"
gh label create "crowdcode:voting" --color "d93f0b"
gh label create "crowdcode:ready-to-promote" --color "0e8a16"
gh label create "crowdcode:promoted" --color "6f42c1"
gh label create "crowdcode:archived" --color "d4c5f9"
```

**Step 4**: Update README
```markdown
# Project Name

[![CrowdCode Enabled](https://img.shields.io/badge/CrowdCode-Enabled-brightgreen)](./CROWDCODE.md)

## CrowdCode Features

This project uses [CrowdCode](./CROWDCODE.md) for collaborative feature development.

- 💡 [Submit a feature idea](../../issues/new?template=feature-request.yml)
- 🗳️ [View voting features](../../pulls?q=is%3Apr+label%3Acrowdcode%3Avoting)
- 🌿 [Browse feature branches](../../branches/all)

See [CROWDCODE.md](./CROWDCODE.md) for more details.
```

**Step 5**: Test Workflow
```bash
# Create test issue
gh issue create --label "crowdcode:feature-request" \
  --title "[FEATURE] Test Feature" \
  --body "Test feature for CrowdCode setup"

# Trigger workflow manually
gh workflow run crowdcode-issue-to-pr.yml
```

### Template Repository

**Create Reusable Template**:
1. Create new repository with CrowdCode structure
2. Remove project-specific code
3. Add template placeholders
4. Enable "Template repository" in settings
5. Users can click "Use this template"

**Template Checklist**:
```markdown
# CrowdCode Template Setup Checklist

After creating repository from template:

- [ ] Update PATCHPANEL_MEMBERS.json with your username
- [ ] Create CrowdCode labels (see CROWDCODE.md)
- [ ] Configure GitHub Pages (optional)
- [ ] Test issue-to-PR workflow
- [ ] Add CrowdCode badge to README
- [ ] Customize crowdcode-config.yml
- [ ] Invite PatchPanel members
```

## ShelfSignals as CrowdCode Reference

### Adaptation Strategy

**Current ShelfSignals Structure**:
```
ShelfSignals/
├── docs/                    # GitHub Pages site
├── scripts/                 # Python analysis tools
├── .github/workflows/       # Current workflows
└── README.md
```

**CrowdCode-Enabled ShelfSignals**:
```
ShelfSignals/
├── docs/
│   └── features/            # NEW: Feature dashboard
├── scripts/
│   ├── (existing scripts)
│   ├── generate-feature-pr.py    # NEW: CrowdCode
│   ├── validate-votes.py         # NEW: CrowdCode
│   └── promote-feature.py        # NEW: CrowdCode
├── .github/
│   ├── workflows/
│   │   ├── (existing workflows)
│   │   ├── crowdcode-issue-to-pr.yml        # NEW
│   │   ├── crowdcode-vote-counting.yml      # NEW
│   │   └── crowdcode-feature-promotion.yml  # NEW
│   ├── ISSUE_TEMPLATE/
│   │   └── feature-request.yml              # NEW
│   ├── PATCHPANEL_MEMBERS.json              # NEW
│   └── crowdcode-config.yml                 # NEW
├── CROWDCODE.md             # NEW: CrowdCode docs
└── README.md                # UPDATE: Add CrowdCode info
```

### Feature Examples for ShelfSignals

**Example 1**: New Visualization
```yaml
name: Interactive Timeline View
description: Add chronological timeline of collection additions
use_case: Visualize collection growth over time
acceptance_criteria:
  - Timeline displays items by year
  - Zoomable and interactive
  - Color-coded by category
```

**Example 2**: Enhanced Search
```yaml
name: Advanced Faceted Search
description: Add multi-field faceted search with live filtering
use_case: Help users find specific items faster
acceptance_criteria:
  - Filter by subject, year, call number
  - Real-time result updates
  - Clear active filter indicators
```

**Example 3**: Export Feature
```yaml
name: Collection Export to CSV
description: Export filtered shelf view to CSV for analysis
use_case: Researchers want to analyze subsets offline
acceptance_criteria:
  - Export button in interface
  - Respects active filters
  - CSV includes all metadata fields
```

## Scripts Reference

### Minimal Script Implementations

**`scripts/generate-feature-pr.py`** (Stub):
```python
#!/usr/bin/env python3
"""
CrowdCode: Generate PRs from feature request issues
"""
import os
import json
from github import Github

def main():
    # Initialize GitHub client
    gh = Github(os.environ['GITHUB_TOKEN'])
    repo = gh.get_repo(os.environ['GITHUB_REPOSITORY'])
    
    # Load config
    with open('.github/crowdcode-config.yml') as f:
        # Parse config (use PyYAML)
        pass
    
    # Find feature request issues
    issues = repo.get_issues(
        state='open',
        labels=['crowdcode:feature-request']
    )
    
    for issue in issues:
        # Check if already has PR
        if 'crowdcode:pending-pr' in [l.name for l in issue.labels]:
            continue
        
        # TODO: Generate code with AI
        # TODO: Create branch
        # TODO: Open PR
        # TODO: Update issue labels
        
        print(f"Generated PR for issue #{issue.number}")

if __name__ == '__main__':
    main()
```

**`scripts/validate-votes.py`** (Stub):
```python
#!/usr/bin/env python3
"""
CrowdCode: Validate and count votes from PatchPanel members
"""
import os
import json
from github import Github

def main():
    gh = Github(os.environ['GITHUB_TOKEN'])
    repo = gh.get_repo(os.environ['GITHUB_REPOSITORY'])
    
    # Load PatchPanel members
    with open('.github/PATCHPANEL_MEMBERS.json') as f:
        data = json.load(f)
        members = [m['github_username'] for m in data['members'] if m['active']]
    
    # Find voting PRs
    prs = repo.get_pulls(
        state='open',
        # Filter by label (requires iteration)
    )
    
    for pr in prs:
        # TODO: Count votes from members
        # TODO: Update PR description
        # TODO: Check promotion threshold
        # TODO: Update labels
        
        print(f"Counted votes for PR #{pr.number}")

if __name__ == '__main__':
    main()
```

**`scripts/promote-feature.py`** (Stub):
```python
#!/usr/bin/env python3
"""
CrowdCode: Promote approved features to main branch
"""
import os
from github import Github

def main():
    gh = Github(os.environ['GITHUB_TOKEN'])
    repo = gh.get_repo(os.environ['GITHUB_REPOSITORY'])
    
    # Find ready-to-promote PRs
    prs = repo.get_pulls(
        state='open',
        # Filter by label
    )
    
    for pr in prs:
        # TODO: Verify vote threshold
        # TODO: Run security checks
        # TODO: Merge PR
        # TODO: Update labels
        # TODO: Close issue
        
        print(f"Promoted PR #{pr.number}")

if __name__ == '__main__':
    main()
```

## Best Practices

1. **Start Minimal**: Begin with basic workflows, add features later
2. **Document Everything**: Clear README and CROWDCODE.md
3. **Test Locally**: Use `act` to test workflows before deploying
4. **Iterate**: Adjust thresholds based on community size
5. **Be Transparent**: Make all decisions public
6. **Secure Credentials**: Use GitHub secrets, never commit tokens
7. **Version Control**: Track config changes in Git
8. **Monitor Usage**: Review workflow runs regularly

## Troubleshooting

**Issue**: Workflows not running
- Check permissions in workflow file
- Verify GitHub Actions enabled in repo settings
- Review workflow run logs

**Issue**: PRs not generated
- Check GITHUB_TOKEN permissions
- Verify issue template format
- Review script logs

**Issue**: Votes not counting
- Verify usernames in PATCHPANEL_MEMBERS.json
- Check label on PR (`crowdcode:voting`)
- Ensure reactions/reviews from members

## Migration Checklist

- [ ] Create `.github/workflows/` directory
- [ ] Add issue-to-pr.yml workflow
- [ ] Add vote-counting.yml workflow
- [ ] Add feature-promotion.yml workflow
- [ ] Create issue template
- [ ] Initialize PATCHPANEL_MEMBERS.json
- [ ] Create crowdcode-config.yml
- [ ] Add generation scripts to `scripts/`
- [ ] Create CrowdCode labels
- [ ] Update README with CrowdCode info
- [ ] Create CROWDCODE.md documentation
- [ ] Test workflow manually
- [ ] Create first test feature request
- [ ] Verify PR generation works
- [ ] Test voting mechanism
- [ ] Document for your team
