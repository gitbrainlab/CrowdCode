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

- 📖 [Architecture Overview](ARCHITECTURE.md)
- 🚀 [Getting Started Guide](docs/GETTING_STARTED.md)
- 🗳️ [Voting Mechanism](docs/VOTING_MECHANISM.md)
- ⚙️ [Workflow Design](docs/WORKFLOW_DESIGN.md)
- 🗺️ [Roadmap](docs/ROADMAP.md)

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

1. **AI as Contributor, Not Authority**: GitHub Copilot generates code, but humans decide what gets merged
2. **Radical Transparency**: All feature branches are public, all votes are visible
3. **Democratic Governance**: PatchPanel members vote on features
4. **Complete Auditability**: Every decision tracked in Git history

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

## Getting Started

### For Users

**Submit a feature request:**
1. Go to [Issues](../../issues/new?template=feature-request.yml)
2. Fill out the feature request form
3. Submit and wait for AI generation
4. Track progress on the PR

### For PatchPanel Members

**Vote on features:**
1. Browse [open PRs](../../pulls?q=is%3Apr+label%3Acrowdcode%3Avoting)
2. Review the implementation
3. Vote using 👍 👎 👀 reactions
4. Or submit formal PR review

### For Maintainers

**Enable CrowdCode in your project:**
1. Copy CrowdCode files to your repo
2. Configure PatchPanel members
3. Create required labels
4. Test with sample feature

See [Getting Started Guide](docs/GETTING_STARTED.md) for detailed instructions.

## Project Status

### Current Phase: Phase 1 - Architecture & Documentation ✅

- [x] Platform architecture designed
- [x] Workflow specifications complete
- [x] Voting mechanism documented
- [x] Repository structure defined
- [x] GitHub Actions workflows created
- [x] Issue templates ready
- [x] Scripts implemented (placeholder)
- [ ] **Next**: AI code generation integration

### Roadmap

- **Phase 1** (Weeks 1-4): Architecture & Documentation ✅
- **Phase 2** (Weeks 5-8): AI Integration & Automation
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

### Core Documentation
- [Architecture Overview](ARCHITECTURE.md) - System design and components
- [Getting Started](docs/GETTING_STARTED.md) - Setup and usage guide
- [Voting Mechanism](docs/VOTING_MECHANISM.md) - How voting works
- [Workflow Design](docs/WORKFLOW_DESIGN.md) - GitHub Actions details
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