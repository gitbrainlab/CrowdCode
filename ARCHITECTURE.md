# CrowdCode Platform Architecture

## Overview

CrowdCode is a collaborative, community-driven software development platform that enables transparent, democratic feature development using GitHub primitives and AI-assisted code generation.

## Core Philosophy

- **AI as Contributor, Not Authority**: GitHub Copilot generates pull requests, but humans decide what gets merged
- **Radical Transparency**: All feature branches remain visible, even if never merged
- **Democratic Governance**: PatchPanel members vote on feature promotion
- **Auditability**: All decisions, votes, and changes are tracked in Git history

## Architecture Components

### 1. Issue-Driven Development

**Feature Requests as GitHub Issues**
- Users submit feature ideas through structured GitHub Issue templates
- Issues are labeled with `crowdcode:feature-request`
- Issues contain structured metadata:
  - Feature description
  - Use case / motivation
  - Acceptance criteria
  - Priority level (optional)

**Issue Metadata**
```yaml
labels:
  - crowdcode:feature-request
  - crowdcode:pending-pr
  - crowdcode:ai-generated
  - crowdcode:voting
  - crowdcode:promoted
```

### 2. Automated PR Generation

**Scheduled Workflow**
- GitHub Actions workflow runs daily (configurable)
- Scans for new issues labeled `crowdcode:feature-request`
- Generates AI-powered pull requests using GitHub Copilot
- Creates dedicated feature branches: `crowdcode/feature-{issue-number}-{slug}`

**PR Generation Process**
1. Parse issue content for requirements
2. Generate code using GitHub Copilot API
3. Create feature branch from main
4. Commit AI-generated code
5. Open PR with reference to original issue
6. Label PR with `crowdcode:ai-generated`
7. Update issue label to `crowdcode:pending-pr`

### 3. Dual-Track Code Evolution

**Main Branch (Canonical)**
- Stable, production-ready code
- Only promoted features are merged here
- Represents community-approved functionality

**Feature Branches (Experimental)**
- Each feature lives on its own branch
- Branches remain visible indefinitely
- Users can test and preview features before voting
- Branches are prefixed: `crowdcode/feature-*`

**Branch Lifecycle**
```
Issue Created → PR Generated → Voting Period → Promotion/Archive
     ↓               ↓              ↓                ↓
  feature/*    Under Review     Voting Open    Merge or Keep
```

### 4. PatchPanel Voting System

**Membership Model**
- PatchPanel: Group of authorized voters
- Members identified by GitHub usernames
- Membership managed via `.github/PATCHPANEL_MEMBERS.json`
- Can be extended with physical codes or tokens

**Vote Mechanisms**

*Initial Implementation (Minimal Infrastructure)*
- Votes cast as PR reviews with specific emoji reactions
- Vote types:
  - 👍 (`:+1:`) = Approve
  - 👎 (`:-1:`) = Reject
  - 👀 (`:eyes:`) = Need more review
- Only PatchPanel members' votes count
- Voting threshold configurable (default: simple majority)

*Future Enhancements*
- Physical code redemption for membership
- Weighted voting based on contribution history
- Time-limited voting windows
- Quadratic voting for feature prioritization

**Vote Validation**
```python
def validate_vote(username, vote_type):
    """Validate vote from PatchPanel member"""
    if username not in patchpanel_members:
        return False, "Not a PatchPanel member"
    
    if vote_type not in ['approve', 'reject', 'review']:
        return False, "Invalid vote type"
    
    return True, "Vote accepted"
```

**Promotion Criteria**
- Minimum quorum (e.g., 3 votes)
- Majority approval (>50% approve votes)
- No blocking concerns (critical security issues)
- Configurable per-repository

### 5. GitHub Primitives Integration

**Issues**
- Feature requests
- Vote tracking
- Discussion threads

**Pull Requests**
- AI-generated code proposals
- Code review platform
- Vote collection mechanism

**Branches**
- Feature isolation
- Parallel development
- Persistent history

**GitHub Actions**
- Scheduled PR generation
- Vote counting automation
- Feature promotion workflow
- Branch cleanup (optional)

**Labels**
- `crowdcode:feature-request` - New feature idea
- `crowdcode:pending-pr` - PR generation in progress
- `crowdcode:ai-generated` - PR created by AI
- `crowdcode:voting` - Active voting period
- `crowdcode:promoted` - Merged to main
- `crowdcode:archived` - Rejected or superseded

**Reactions**
- Vote collection (👍 👎 👀)
- Quick feedback mechanism

### 6. Transparency & Auditability

**Public Visibility**
- All PRs are public
- All votes are visible
- All branches are accessible
- Git history tracks all changes

**Audit Trail**
- Issue creation timestamp
- PR generation timestamp
- Vote timestamps and authors
- Promotion/rejection decisions
- Complete Git history

**Reporting**
- Vote summary in PR description
- Feature dashboard (GitHub Pages)
- Activity feed (RSS/JSON)

## Data Flow

```
┌─────────────────┐
│  User submits   │
│  GitHub Issue   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Daily GitHub Actions   │
│  Workflow Triggered     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  AI Generates Code      │
│  (GitHub Copilot API)   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Create Feature Branch  │
│  crowdcode/feature-N    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Open Pull Request      │
│  Link to Issue          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  PatchPanel Members     │
│  Review & Vote          │
└────────┬────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│Approved│ │ Rejected │
└───┬────┘ └────┬─────┘
    │           │
    ▼           ▼
┌────────┐ ┌──────────┐
│ Merge  │ │  Archive │
│to main │ │  Branch  │
└────────┘ └──────────┘
```

## Technology Stack

### Core Infrastructure
- **Git**: Version control and history
- **GitHub**: Hosting, Issues, PRs, Actions
- **GitHub Copilot**: AI code generation
- **GitHub Actions**: Automation and workflows

### Scripting & Automation
- **Python**: Vote validation, PR generation
- **YAML**: Workflow configuration
- **JSON**: Data storage (PatchPanel members, config)

### Future Extensions
- **GitHub Pages**: Dashboard and reporting
- **GitHub GraphQL API**: Advanced queries
- **Webhook Integration**: Real-time notifications

## Security Considerations

### Vote Integrity
- Only PatchPanel members can vote
- Votes are cryptographically signed (via GitHub auth)
- Vote history is immutable (Git)

### Code Security
- All AI-generated code is reviewable
- CodeQL scanning on all PRs
- Dependency security checks
- Human approval required for merge

### Membership Management
- PatchPanel membership is explicit
- Changes to membership are auditable
- Physical codes stored securely (future)

## Scalability

### Small Projects (1-10 features/month)
- Manual vote counting acceptable
- Simple majority voting
- Human-triggered promotion

### Medium Projects (10-50 features/month)
- Automated vote counting
- Scheduled promotion workflows
- Dashboard for tracking

### Large Projects (50+ features/month)
- Priority queues for PR generation
- Advanced voting mechanisms (quadratic, weighted)
- Automated testing before voting
- Feature branch cleanup policies

## Extension Points

### Custom AI Models
- Pluggable code generation backends
- Fine-tuned models for specific domains
- Multi-model consensus for complex features

### Advanced Voting
- Time-weighted votes (decay over time)
- Reputation-based voting power
- Delegation and proxy voting
- Quadratic voting for resource allocation

### Integration Hooks
- Slack/Discord notifications
- External dashboards
- Analytics and metrics
- Custom deployment pipelines

## Migration Path

### Phase 1: Core Platform (MVP)
- Issue templates
- Basic PR generation workflow
- Simple voting (reactions)
- Manual promotion

### Phase 2: Automation
- Automated vote counting
- Scheduled workflows
- Auto-promotion on threshold
- Branch visibility dashboard

### Phase 3: Advanced Features
- Physical code integration
- Weighted voting
- Advanced analytics
- Template repository

### Phase 4: Ecosystem
- CrowdCode CLI tool
- Plugin system
- Community templates
- Multi-repository orchestration

## Success Metrics

- **Participation**: Number of feature requests submitted
- **Velocity**: Time from issue to PR
- **Quality**: Percentage of promoted features that remain stable
- **Engagement**: PatchPanel member vote participation rate
- **Transparency**: Public visibility of all decisions
- **Adoption**: Number of projects using CrowdCode

## Principles

1. **Openness**: All code, all votes, all decisions are public
2. **Traceability**: Complete audit trail in Git history
3. **Community Trust**: Democracy over autocracy
4. **AI Augmentation**: AI assists, humans decide
5. **Simplicity**: Start minimal, extend as needed
6. **Portability**: Easy to adopt in any GitHub repository
