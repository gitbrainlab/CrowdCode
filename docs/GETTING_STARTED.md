# Getting Started with CrowdCode

This guide will help you enable CrowdCode in a new or existing repository.

## What is CrowdCode?

CrowdCode is a collaborative software development platform that enables:
- 💡 **Community Feature Requests** via GitHub Issues
- 🤖 **AI-Powered Implementation** via GitHub Copilot
- 🗳️ **Democratic Voting** via PatchPanel membership
- 🌿 **Transparent Development** with public feature branches

## Quick Start

### 1. Install CrowdCode Files

Copy the CrowdCode files to your repository:

```bash
# Create directories
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p scripts
mkdir -p docs/features

# Copy workflow files (from this repository)
cp .github/workflows/crowdcode-*.yml your-repo/.github/workflows/

# Copy configuration files
cp .github/ISSUE_TEMPLATE/feature-request.yml your-repo/.github/ISSUE_TEMPLATE/
cp .github/PATCHPANEL_MEMBERS.json your-repo/.github/
cp .github/crowdcode-config.yml your-repo/.github/

# Copy scripts
cp scripts/*.py your-repo/scripts/
```

### 2. Configure PatchPanel Membership

Edit `.github/PATCHPANEL_MEMBERS.json` to add initial members:

```json
{
  "version": "1.0",
  "updated": "2025-12-21T21:00:00Z",
  "members": [
    {
      "github_username": "your-username",
      "joined": "2025-12-21T21:00:00Z",
      "role": "founding",
      "active": true,
      "notes": "Project founder"
    }
  ]
}
```

### 3. Create GitHub Labels

Create the required labels in your repository:

```bash
# Using GitHub CLI
gh label create "crowdcode:feature-request" --color "0e8a16" --description "New feature idea"
gh label create "crowdcode:pending-pr" --color "fbca04" --description "PR generation in progress"
gh label create "crowdcode:ai-generated" --color "0075ca" --description "Created by AI"
gh label create "crowdcode:voting" --color "d93f0b" --description "Active voting period"
gh label create "crowdcode:ready-to-promote" --color "0e8a16" --description "Approved, ready to merge"
gh label create "crowdcode:promoted" --color "6f42c1" --description "Merged to main"
gh label create "crowdcode:archived" --color "d4c5f9" --description "Rejected or superseded"
```

Or create them manually in your repository settings under Issues > Labels.

### 4. Update README

Add CrowdCode information to your README.md:

```markdown
# Your Project

[![CrowdCode Enabled](https://img.shields.io/badge/CrowdCode-Enabled-brightgreen)](./CROWDCODE.md)

## Features

This project uses [CrowdCode](./CROWDCODE.md) for collaborative feature development.

- 💡 [Submit a feature idea](../../issues/new?template=feature-request.yml)
- 🗳️ [View voting features](../../pulls?q=is%3Apr+label%3Acrowdcode%3Avoting)
- 🌿 [Browse feature branches](../../branches/all)
```

### 5. Test the Setup

Create a test feature request:

```bash
gh issue create \
  --label "crowdcode:feature-request" \
  --title "[FEATURE] Test Feature" \
  --body "This is a test feature to verify CrowdCode is working."
```

Or use the issue template in your browser:
- Go to your repository
- Click "Issues" > "New Issue"
- Select "CrowdCode Feature Request"
- Fill out the form

### 6. Trigger Workflows

Manually trigger the workflows to test:

```bash
# Test PR generation
gh workflow run crowdcode-issue-to-pr.yml

# Check workflow status
gh run list --workflow=crowdcode-issue-to-pr.yml
```

## Configuration

### Voting Thresholds

Edit `.github/crowdcode-config.yml` to adjust voting:

```yaml
voting:
  quorum: 3                    # Minimum votes required (adjust for team size)
  approval_threshold: 0.5      # 50% approval needed (0.0 to 1.0)
  voting_period_days: 7        # How long voting stays open
```

**Recommendations**:
- **Small teams (2-5)**: `quorum: 2`, `threshold: 0.5`
- **Medium teams (6-20)**: `quorum: 3`, `threshold: 0.5`
- **Large teams (20+)**: `quorum: 5`, `threshold: 0.6`

### Merge Strategy

Configure how features are merged:

```yaml
promotion:
  merge_method: "squash"       # Options: merge, squash, rebase
  require_tests: true          # Require passing tests
  require_codeql: false        # Require security scan
  auto_delete_branch: false    # Keep branches visible
```

## Workflow Overview

1. **User submits feature request** via GitHub Issue
2. **Daily workflow** scans for new issues
3. **AI generates code** (Phase 2 - coming soon)
4. **PR created automatically** with AI implementation
5. **PatchPanel members vote** using reactions or reviews
6. **Vote counting** runs hourly
7. **Feature promoted** when threshold met
8. **Branch remains visible** for transparency

## Voting Guide

### For Voters

To vote on a feature PR:

1. Go to the Pull Request
2. React to the PR description:
   - 👍 = Approve (merge this feature)
   - 👎 = Reject (don't merge)
   - 👀 = Need more review

Or submit a formal review:
- **Approve** = Strong support
- **Request Changes** = Blocking concerns
- **Comment** = Feedback without blocking

Only votes from PatchPanel members count toward promotion.

### Vote Counting

Votes are counted automatically every hour. The PR description shows:
- Current vote tally
- Approval rate
- Quorum status
- Ready to promote status

## Adding PatchPanel Members

### Method 1: Direct Addition

Edit `.github/PATCHPANEL_MEMBERS.json`:

```json
{
  "members": [
    {
      "github_username": "new-member",
      "joined": "2025-12-21T21:00:00Z",
      "role": "contributor",
      "active": true,
      "notes": "Active contributor"
    }
  ]
}
```

Commit and push the changes.

### Method 2: Physical Codes (Future)

Enable physical code redemption:

```yaml
# In .github/crowdcode-config.yml
patchpanel:
  require_physical_codes: true
```

Users can redeem codes via issues to join PatchPanel.

## Troubleshooting

### Workflows Not Running

**Problem**: Workflows don't trigger automatically

**Solutions**:
- Check GitHub Actions is enabled in repository settings
- Verify workflow files have correct permissions
- Check workflow run logs for errors
- Try manual trigger: `gh workflow run crowdcode-issue-to-pr.yml`

### Votes Not Counting

**Problem**: Reactions/reviews don't update vote count

**Solutions**:
- Verify username is in PATCHPANEL_MEMBERS.json
- Check spelling of username (case-sensitive)
- Ensure `active: true` in member record
- Verify PR has `crowdcode:voting` label
- Wait for hourly vote counting workflow

### Labels Missing

**Problem**: CrowdCode labels don't exist

**Solutions**:
- Create labels manually or via `gh label create`
- Check label names match config exactly
- Labels are case-sensitive

### PRs Not Generated

**Problem**: Issues don't create PRs

**Solutions**:
- Verify issue has `crowdcode:feature-request` label
- Check workflow run logs for errors
- Ensure GITHUB_TOKEN has sufficient permissions
- Try dry-run mode: `gh workflow run crowdcode-issue-to-pr.yml -f dry_run=true`

## Best Practices

### For Project Maintainers

1. **Start Small**: Begin with 2-3 PatchPanel members
2. **Communicate Clearly**: Explain CrowdCode to contributors
3. **Set Expectations**: Document voting process in CONTRIBUTING.md
4. **Monitor Activity**: Review workflow runs weekly
5. **Iterate**: Adjust thresholds based on team size and activity

### For PatchPanel Members

1. **Vote Promptly**: Review PRs within voting period
2. **Provide Feedback**: Comment on concerns or suggestions
3. **Be Constructive**: Explain rejection reasons
4. **Test Features**: Try out code before voting
5. **Stay Active**: Participate regularly in voting

### For Feature Requesters

1. **Be Specific**: Provide detailed descriptions
2. **Define Success**: Include acceptance criteria
3. **Explain Value**: Describe use case and motivation
4. **Be Patient**: AI generation takes time
5. **Engage**: Respond to questions and feedback

## Next Steps

1. ✅ Install CrowdCode files
2. ✅ Configure PatchPanel members
3. ✅ Create labels
4. ✅ Test with sample issue
5. 📖 Read [ARCHITECTURE.md](../ARCHITECTURE.md)
6. 📖 Read [VOTING_MECHANISM.md](VOTING_MECHANISM.md)
7. 📖 Read [WORKFLOW_DESIGN.md](WORKFLOW_DESIGN.md)
8. 🚀 Start using CrowdCode for real features!

## Resources

- [CrowdCode Architecture](../ARCHITECTURE.md)
- [Workflow Design](WORKFLOW_DESIGN.md)
- [Voting Mechanism](VOTING_MECHANISM.md)
- [Repository Structure](REPO_STRUCTURE.md)
- [Roadmap](ROADMAP.md)

## Getting Help

- 📖 Check documentation in `docs/` directory
- 🐛 Open an issue for bugs
- 💬 Start a discussion for questions
- 📧 Contact project maintainers

## Example Projects

- [CrowdCode](https://github.com/evcatalyst/CrowdCode) - Reference implementation
- [ShelfSignals](https://github.com/evcatalyst/ShelfSignals) - Pilot project (coming soon)

---

**Welcome to CrowdCode!** 🎉

By enabling democratic, AI-assisted development, you're joining a community that values transparency, collaboration, and innovation.
