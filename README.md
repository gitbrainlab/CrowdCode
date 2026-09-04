# CrowdCode

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CrowdCode](https://img.shields.io/badge/CrowdCode-Enabled-brightgreen)](./ARCHITECTURE.md)

> **Democratic, AI-Assisted Software Development**

CrowdCode is a collaborative platform for community-driven software development using GitHub primitives and AI-powered code generation. It enables transparent, democratic feature development where:

- 💡 **Anyone can propose** features via GitHub Issues
- 🤖 **AI generates** pull requests automatically
- 🗳️ **Community votes** on which features to promote
- 🌿 **All branches remain visible**, even if not merged

## Quick Links

### Documentation
- 📚 **[Documentation Hub](docs/index.md)** - Start here for complete guide
- 🚀 **[Setup Guide](docs/setup.md)** - Install CrowdCode in your repo
- ⚙️ **[Workflows Reference](docs/workflows.md)** - Automation details
- 🗳️ **[Governance Guide](docs/governance.md)** - Voting and PatchPanel
- 🛡️ **[Threat Model](docs/threat-model.md)** - Security considerations

### Reference
- 📖 [Architecture Overview](ARCHITECTURE.md)
- 🗺️ [Roadmap](docs/ROADMAP.md)
- 📝 [Contributing](CONTRIBUTING.md)

## What is CrowdCode?

CrowdCode transforms how open source projects handle feature requests:

**Traditional Approach:**
```
Feature Request → Maintainer Reviews → Maintainer Codes → Manual Merge
```

**CrowdCode Approach:**
```
Feature Request → AI Generates PR → Community Votes → Automatic Promotion
```

### Key Principles

1. **AI as Contributor, Not Authority**: AI generates code proposals, but humans decide what gets merged
2. **Radical Transparency**: All feature branches are public, all votes are visible
3. **Democratic Governance**: PatchPanel members vote on features
4. **Complete Auditability**: Every decision tracked in Git history
5. **Safety First**: AI code requires review; every automation has an off switch

## Core Features

### 🎯 Issue-Driven Development

Submit feature requests using structured GitHub Issue templates. Each request includes:
- Feature description
- Use case and motivation
- Acceptance criteria
- Priority level

### 🤖 AI-Powered PR Generation

Scheduled GitHub Actions workflows:
- Scan for new feature requests daily
- Generate code using GitHub Copilot (Phase 2)
- Create feature branches automatically
- Open pull requests with implementation

### 🗳️ PatchPanel Voting System

**PatchPanel**: Authorized voter group who decides feature promotion

- Vote using GitHub reactions (👍 👎 👀) or PR reviews
- Configurable quorum and approval thresholds
- Real-time vote counting
- Transparent voting records

### 🌿 Dual-Track Development

**Main Branch**: Stable, production-ready code with promoted features

**Feature Branches**: Experimental implementations, all publicly visible
- Format: `crowdcode/feature-{issue-number}-{slug}`
- Never auto-deleted
- Can be tested independently
- Remain visible even if rejected

## How It Works

### 1. Submit Feature Request

Use the GitHub Issue template to propose a feature:

```markdown
Feature Name: Dark Mode Support
Description: Add dark theme toggle to all interfaces
Use Case: Improve accessibility and reduce eye strain
Acceptance Criteria:
- [ ] Toggle button in header
- [ ] Theme persists in localStorage
- [ ] All UI elements have dark variants
```

### 2. AI Generates Implementation

Daily workflow scans for new requests and:
- Creates feature branch
- Generates code implementation
- Opens pull request
- Links PR to original issue

### 3. Community Reviews and Votes

PatchPanel members:
- Review the AI-generated code
- Provide feedback and suggestions
- Vote on whether to promote

Vote methods:
- 👍 Reaction = Approve
- 👎 Reaction = Reject
- 👀 Reaction = Need more review
- PR Reviews (Approve/Request Changes)

### 4. Automatic Promotion

When voting threshold is met:
- Feature is merged to main
- Original issue is closed
- Feature branch remains visible
- Changelog is updated

## Try It Quickly

### 🚀 Safe Trial (Recommended)

Trial CrowdCode in a test repository before production use:

```bash
# 1. Create a test repository
gh repo create my-org/crowdcode-trial --public --clone
cd crowdcode-trial

# 2. Copy CrowdCode files
# See detailed setup: docs/setup.md

# 3. Configure with conservative settings
# - Small PatchPanel (2-3 trusted members)
# - AI generation disabled initially
# - Manual workflow triggers only

# 4. Test with sample feature request
# 5. Verify voting and promotion work as expected
# 6. Deploy to production once comfortable
```

**⚠️ Important**: Read the [Threat Model](docs/threat-model.md) before enabling in production.

**📖 Full Installation**: See [Setup Guide](docs/setup.md) for step-by-step instructions.

### For Users

**Submit a feature request:**
1. Go to [Issues](../../issues/new?template=feature-request.yml)
2. Fill out the feature request form
3. Submit and wait for AI generation
4. Track progress on the PR

### For PatchPanel Members

**Vote on features:**
1. Browse [open PRs](../../pulls?q=is%3Apr+label%3Acrowdcode%3Avoting)
2. Review the implementation (AI code requires human approval)
3. Vote using 👍 👎 👀 reactions
4. Or submit formal PR review

### For Maintainers

**Enable CrowdCode in your project:**
1. Copy CrowdCode files to your repo
2. Configure PatchPanel members
3. Create required labels
4. Test with sample feature

See **[Setup Guide](docs/setup.md)** for detailed instructions.

## Project Status

### Current Phase: Phase 1 - Architecture & Documentation ✅

**Ready for Trial Adoption**

CrowdCode is ready for safe trial in test repositories. The workflow infrastructure is complete, with AI integration planned for Phase 2.

**What's Working Now:**
- ✅ Complete workflow automation (issue → PR → vote → promote)
- ✅ PatchPanel voting system
- ✅ Branch visibility and transparency
- ✅ Manual PR creation and review
- ✅ Comprehensive documentation with security focus

**What's Coming (Phase 2):**
- 🔜 AI-powered code generation
- 🔜 Automated PR creation from issues
- 🔜 Enhanced security scanning

**Current Status:**
- [x] Platform architecture designed
- [x] Workflow specifications complete
- [x] Voting mechanism documented
- [x] Repository structure defined
- [x] GitHub Actions workflows created
- [x] Issue templates ready
- [x] Scripts implemented (placeholder)
- [x] **Comprehensive documentation** (Setup, Workflows, Governance, Threat Model)
- [ ] **Next**: AI code generation integration

### Roadmap

- **Phase 1** (Weeks 1-4): Architecture & Documentation ✅ **COMPLETE**
- **Phase 2** (Weeks 5-8): AI Integration & Automation 🔜 **NEXT**
- **Phase 3** (Weeks 9-16): Generalization & Templates
- **Phase 4** (Weeks 17-24): Ecosystem Development
- **Phase 5** (Months 6-12): Platform Maturity

See [ROADMAP.md](docs/ROADMAP.md) for complete roadmap.

## Components

### GitHub Actions Workflows

- **`crowdcode-issue-to-pr.yml`**: Converts issues to PRs (daily)
- **`crowdcode-vote-counting.yml`**: Counts PatchPanel votes (hourly)
- **`crowdcode-feature-promotion.yml`**: Promotes approved features (daily)
- **`crowdcode-branch-visibility.yml`**: Maintains feature dashboard (weekly)

### Configuration Files

- **`.github/PATCHPANEL_MEMBERS.json`**: Authorized voters list
- **`.github/crowdcode-config.yml`**: Platform configuration
- **`.github/ISSUE_TEMPLATE/feature-request.yml`**: Feature request form

### Scripts

- **`generate-feature-pr.py`**: Generate PRs from issues
- **`validate-votes.py`**: Count and validate votes
- **`promote-feature.py`**: Merge approved features
- **`generate-dashboard.py`**: Build feature dashboard

## Use Cases

### Open Source Projects

Enable community-driven feature development:
- Anyone can propose features
- AI handles initial implementation
- Community decides what to include
- Transparent decision-making

### Research Projects

Collaborative tool development:
- Researchers propose analysis features
- AI generates code scaffolding
- Expert panel votes on inclusion
- All experiments remain visible

### Educational Projects

Student-driven development:
- Students propose features
- AI assists with implementation
- Instructors guide via voting
- Learning artifacts preserved

### Exhibition/Installation Projects

Public participation in software:
- Exhibition visitors propose features via codes
- Real-time development during exhibition
- Community shapes the tool
- Digital democracy in action

## Philosophy

CrowdCode is built on the belief that:

1. **Communities should shape their tools** rather than being shaped by them
2. **AI should augment human creativity**, not replace human judgment
3. **Transparency builds trust** more than speed builds adoption
4. **Code should be visible** even when not deployed
5. **Democracy scales** when properly designed

## Inspiration

CrowdCode was conceived for [ShelfSignals](https://github.com/evcatalyst/ShelfSignals), a library analytics and visualization platform. The goal was to enable:

- Library patrons to propose features
- Exhibition visitors to participate via physical codes
- AI to assist with implementation
- Community to decide direction

The platform is now being generalized for any collaborative software project.

## Documentation

### New: Maintainer-Focused Documentation

**Essential Reading:**
- **[Documentation Hub](docs/index.md)** - Overview, glossary, and navigation
- **[Setup Guide](docs/setup.md)** - Install CrowdCode safely in your repository
- **[Workflows Reference](docs/workflows.md)** - Complete automation guide with disable instructions
- **[Governance Guide](docs/governance.md)** - PatchPanel membership and voting
- **[Threat Model](docs/threat-model.md)** - Security analysis and mitigations

**Key Features:**
- ✅ Emphasis on safety and control
- ✅ Every automation has an "off switch"
- ✅ Data privacy documentation
- ✅ Abuse and security considerations
- ✅ Role definitions (proposer, voter, maintainer)

### Reference Documentation
- [Architecture Overview](ARCHITECTURE.md) - System design and components
- [Getting Started](docs/GETTING_STARTED.md) - Original setup guide
- [Voting Mechanism](docs/VOTING_MECHANISM.md) - Detailed voting mechanics
- [Workflow Design](docs/WORKFLOW_DESIGN.md) - Original workflow specs
- [Repository Structure](docs/REPO_STRUCTURE.md) - File organization
- [Roadmap](docs/ROADMAP.md) - Evolution plan

## Contributing

We welcome contributions! CrowdCode itself uses CrowdCode for development (meta!).

Ways to contribute:
- 💡 [Submit feature requests](../../issues/new?template=feature-request.yml)
- 🗳️ Join the PatchPanel (request membership)
- 🐛 Report bugs
- 📖 Improve documentation
- 💻 Submit pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines (coming soon).

## License

MIT License - See [LICENSE](LICENSE) for details

## Authors

Created by [evcatalyst](https://github.com/evcatalyst) for collaborative, democratic software development.

## Acknowledgments

- **ShelfSignals**: Reference implementation
- **GitHub Copilot**: AI code generation
- **GitHub Actions**: Automation infrastructure
- **Open Source Community**: Inspiration and principles

---

**CrowdCode**: Where AI proposes, humans decide, and transparency wins. 🚀