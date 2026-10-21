# CrowdCode Documentation

> **GitHub-native, vote-gated, AI-assisted development workflow**

## What is CrowdCode?

CrowdCode is a collaborative platform for **community-driven software development** that combines GitHub primitives with AI code generation. It enables transparent, democratic feature development where:

- 💡 **Anyone can propose** features via GitHub Issues
- 🤖 **AI generates** implementation proposals (reviewed, not auto-merged)
- 🗳️ **Community votes** on which features to promote
- 🌿 **All branches remain visible**, even if rejected
- 🛡️ **Human control** is maintained at every step

## Critical Principle

**AI-generated code is a PROPOSAL that must be reviewed and approved by humans before merging.** CrowdCode emphasizes controls, transparency, and human decision-making over automation speed.

## Glossary

| Term | Definition |
|------|------------|
| **Feature Request** | GitHub Issue proposing a new feature, labeled `crowdcode:feature-request` |
| **AI-Generated PR** | Pull request created by AI from a feature request (requires human approval) |
| **PatchPanel** | Authorized group of voters who decide feature promotion |
| **Voting** | Democratic process where PatchPanel members approve/reject PRs |
| **Promotion** | Merging an approved feature PR into the main branch |
| **Feature Branch** | Permanent branch containing a feature implementation (`crowdcode/feature-*`) |
| **Proposer** | User who submits a feature request issue |
| **Voter** | PatchPanel member who reviews and votes on PRs |
| **Maintainer/Operator** | Repository owner who configures and monitors CrowdCode |

## Workflow Overview

```
Issue → AI Generates PR → PatchPanel Votes → Human Reviews → Promote
  ↓           ↓                   ↓                ↓             ↓
Feature    Proposal         Democratic        Safety      Merge or
Request    Created          Decision          Check       Archive
```

### Step-by-Step Process

1. **Issue Creation** (Proposer)
   - User submits feature request via GitHub Issue template
   - Issue is labeled `crowdcode:feature-request`
   
2. **PR Generation** (Automated, Daily)
   - Workflow scans for new feature requests
   - AI generates code implementation
   - PR created with label `crowdcode:ai-generated`
   - **Safety**: Human review required before any merge

3. **Voting Period** (Voters)
   - PatchPanel members review AI-generated code
   - Vote using reactions (👍 approve, 👎 reject, 👀 review needed)
   - Vote counting runs hourly
   - **Safety**: Only authorized voters can approve

4. **Promotion Decision** (Automated, Gated)
   - When quorum + threshold met, PR labeled `crowdcode:ready-to-promote`
   - Daily workflow checks for approved PRs
   - **Safety**: Additional checks run before merge (tests, security scans)
   - Approved PR merged to main, branch preserved

5. **Branch Visibility** (Automated, Weekly)
   - All feature branches indexed
   - Dashboard updated with status
   - **Safety**: Rejected features remain visible for transparency

## Roles and Responsibilities

### Proposer (Any User)
- Submits feature requests via GitHub Issues
- Provides clear requirements and acceptance criteria
- Responds to questions during review
- **Cannot**: Auto-merge, bypass voting, or modify other issues

### Voter (PatchPanel Member)
- Reviews AI-generated PRs for correctness and safety
- Votes on feature promotion (approve/reject)
- Provides constructive feedback
- **Cannot**: Bypass security checks or merge without quorum

### Maintainer/Operator (Repository Owner)
- Configures CrowdCode (thresholds, schedules, permissions)
- Manages PatchPanel membership
- Monitors automation for issues
- **Can**: Disable workflows, override decisions, modify configuration
- **Should**: Regularly audit activity and review security alerts

## Safety and Abuse Considerations

### Potential Threats
- ✋ Malicious feature requests (prompt injection, backdoors)
- ✋ Spam issues overwhelming the queue
- ✋ Malicious PRs from compromised AI
- ✋ Vote manipulation or Sybil attacks
- ✋ Dependency confusion attacks
- ✋ Model hallucinations creating buggy code

### Mitigations
- ✅ **Human review required** - AI code never auto-merges
- ✅ **Restricted voter group** - Only PatchPanel members can approve
- ✅ **Rate limiting** - Maximum issues processed per run (default: 5)
- ✅ **CI/CD gates** - Tests and security scans before promotion
- ✅ **Audit trail** - All votes and decisions in Git history
- ✅ **Disable switches** - Every automation has an off switch
- ✅ **Branch preservation** - Rejected features remain visible for investigation

See [Threat Model](threat-model.md) for detailed security analysis.

## Documentation Structure

### Getting Started
- **[Setup Guide](setup.md)** - Install CrowdCode in your repository
  - Files to copy, configurations to set
  - Labels, permissions, secrets required
  - Testing and verification steps

### Understanding the System
- **[Workflows](workflows.md)** - GitHub Actions automation details
  - What each workflow does
  - Inputs, outputs, schedules
  - How to disable or customize

- **[Governance](governance.md)** - Voting and decision-making
  - PatchPanel membership management
  - Vote counting and thresholds
  - Conflict resolution procedures

### Security and Safety
- **[Threat Model](threat-model.md)** - Security considerations
  - Attack scenarios and mitigations
  - Data privacy and model provider usage
  - Incident response procedures

### Reference Documentation
- **[Architecture](../ARCHITECTURE.md)** - Technical design overview
- **[Contributing](../CONTRIBUTING.md)** - How to contribute to CrowdCode itself
- **[Roadmap](ROADMAP.md)** - Future development plans

## Quick Links

- 🚀 **[Try CrowdCode](setup.md#quick-trial)** - Safe trial in a test repository
- 🗳️ **[Understanding Voting](governance.md)** - How decisions are made
- 🛡️ **[Security Guide](threat-model.md)** - Safety considerations
- ⚙️ **[Workflow Reference](workflows.md)** - Automation details
- 📖 **[Full README](../README.md)** - Project overview

## Data and Privacy

### What Data Goes to Model Providers
When AI generation is enabled (`ai_generation.enabled: true`):
- ✅ **Sent**: Issue title, description, acceptance criteria
- ✅ **Sent**: Repository context (file structure, relevant code)
- ✅ **Sent**: Code generation prompts

### What Should NEVER Be Sent
- ❌ Secrets, credentials, API keys
- ❌ Personal user data (emails, names unless public)
- ❌ Proprietary or confidential code
- ❌ PatchPanel member lists
- ❌ Vote tallies or decisions

**Recommendation**: Review AI provider's data usage policy before enabling AI generation.

## Control and Off Switches

Every automation in CrowdCode can be disabled:

| Component | How to Disable |
|-----------|----------------|
| **All workflows** | Delete or rename `.github/workflows/crowdcode-*.yml` |
| **PR generation** | Set `ai_generation.enabled: false` in config |
| **Vote counting** | Delete `crowdcode-vote-counting.yml` workflow |
| **Auto-promotion** | Delete `crowdcode-feature-promotion.yml` workflow |
| **Dashboard updates** | Delete `crowdcode-branch-visibility.yml` workflow |
| **Issue processing** | Remove `crowdcode:feature-request` label |

See [Workflows](workflows.md#disabling-workflows) for detailed instructions.

## Project Status

**Current Phase**: Phase 1 - Architecture & Documentation ✅

CrowdCode is ready for trial adoption with manual review processes. AI integration (Phase 2) is planned but not yet implemented, making this an ideal time to trial the workflow with human-generated PRs.

See [Roadmap](ROADMAP.md) for development timeline.

## Getting Help

- 📖 Read the [Setup Guide](setup.md) for installation
- 🔍 Check [Workflows](workflows.md) for automation details
- 🗳️ Review [Governance](governance.md) for voting mechanics
- 🛡️ Read [Threat Model](threat-model.md) for security
- 🐛 [Open an issue](https://github.com/gitbrainlab/CrowdCode/issues) for bugs
- 💬 [Start a discussion](https://github.com/gitbrainlab/CrowdCode/discussions) for questions

---

**Next**: Read the [Setup Guide](setup.md) to install CrowdCode in your repository.
