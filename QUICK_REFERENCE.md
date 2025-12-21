# CrowdCode Quick Reference

## 🚀 Quick Start

```bash
# Submit a feature request
Open issue: https://github.com/evcatalyst/CrowdCode/issues/new?template=feature-request.yml

# View active votes
Browse PRs: https://github.com/evcatalyst/CrowdCode/pulls?q=is%3Apr+label%3Acrowdcode%3Avoting

# Check all features
See branches: https://github.com/evcatalyst/CrowdCode/branches/all
```

## 🗳️ Voting

| Action | Method |
|--------|--------|
| Approve | 👍 reaction or "Approve" review |
| Reject | 👎 reaction or "Request changes" review |
| Need Review | 👀 reaction or "Comment" review |

Only PatchPanel members' votes count!

## 🏷️ Labels

| Label | Meaning |
|-------|---------|
| `crowdcode:feature-request` | New feature idea submitted |
| `crowdcode:pending-pr` | PR being generated |
| `crowdcode:ai-generated` | PR created by AI |
| `crowdcode:voting` | Voting in progress |
| `crowdcode:ready-to-promote` | Approved, will merge soon |
| `crowdcode:promoted` | Merged to main branch |
| `crowdcode:archived` | Rejected or superseded |

## ⚙️ Workflows

| Workflow | Schedule | Purpose |
|----------|----------|---------|
| issue-to-pr | Daily 2 AM UTC | Generate PRs from issues |
| vote-counting | Hourly | Count and update votes |
| feature-promotion | Daily 6 AM UTC | Merge approved features |
| branch-visibility | Weekly | Update feature dashboard |

## 📋 Default Settings

```yaml
Voting:
  Quorum: 3 votes
  Approval: 50%
  Period: 7 days

Promotion:
  Method: squash
  Auto-delete: false (keep branches visible)
```

## 🔧 Configuration Files

- `.github/crowdcode-config.yml` - Platform settings
- `.github/PATCHPANEL_MEMBERS.json` - Authorized voters
- `.github/ISSUE_TEMPLATE/feature-request.yml` - Feature template

## 📚 Documentation

- `README.md` - Platform overview
- `ARCHITECTURE.md` - System design
- `docs/GETTING_STARTED.md` - Setup guide
- `docs/VOTING_MECHANISM.md` - How voting works
- `docs/WORKFLOW_DESIGN.md` - Workflow details
- `docs/REPO_STRUCTURE.md` - File organization
- `docs/ROADMAP.md` - Future plans
- `CONTRIBUTING.md` - How to contribute
- `IMPLEMENTATION_SUMMARY.md` - What's been built

## 🐍 Scripts

All in `scripts/` directory:

- `generate-feature-pr.py` - Create PRs from issues
- `validate-votes.py` - Count PatchPanel votes
- `promote-feature.py` - Merge approved features
- `generate-dashboard.py` - Build feature list

## 🎯 Feature Lifecycle

```
1. Issue Created
   ↓
2. PR Generated (daily)
   ↓
3. Voting Opens (PatchPanel)
   ↓
4. Votes Counted (hourly)
   ↓
5. Threshold Met?
   ↓ YES
6. Feature Promoted (daily)
   ↓
7. Branch Preserved (forever)
```

## 💡 Tips

**For Requesters:**
- Be specific in descriptions
- Include use cases
- Define acceptance criteria
- Be patient (AI generation takes time)

**For Voters:**
- Review code carefully
- Vote promptly
- Explain rejections
- Test when possible

**For Maintainers:**
- Adjust thresholds for team size
- Monitor workflow runs
- Keep PatchPanel updated
- Communicate with community

## 🔐 Security

- All scripts scanned: ✅ 0 vulnerabilities
- Votes validated: ✅ PatchPanel only
- Code reviewed: ✅ Human oversight required
- Audit trail: ✅ Complete Git history

## 📊 Project Stats

- **Files**: 27 (excluding .git)
- **Lines**: 5,173 (code + docs)
- **Documentation**: 9 comprehensive guides
- **Workflows**: 4 automated processes
- **Scripts**: 4 Python utilities
- **Templates**: 1 feature request form

## 🌟 Key Innovations

1. **AI as Contributor** - Generates proposals, not final code
2. **Radical Transparency** - All branches visible forever
3. **Democratic Governance** - Community votes decide
4. **Physical Codes** - Real-world participation (PATCH-2025-NNNN)

## 📞 Getting Help

- 📖 Read the docs in `docs/` directory
- 🐛 Open an issue for bugs
- 💬 Start a discussion for questions
- 📧 Contact @evcatalyst

## 🎓 Philosophy

> **CrowdCode**: Where AI proposes, humans decide, and transparency wins.

### Core Principles

1. **Openness**: All code, votes, decisions public
2. **Traceability**: Complete audit trail
3. **Community Trust**: Democracy over autocracy
4. **AI Augmentation**: Assists, doesn't replace
5. **Simplicity**: Minimal infrastructure, maximum impact

## 🚦 Status

**Current Phase**: Phase 1 Complete ✅

**Next Phase**: AI Integration (Phase 2)

**Ready For**: Setup in new repositories, testing, refinement

---

**License**: MIT | **Version**: 1.0.0 | **Updated**: 2025-12-21
