# CrowdCode Voting Mechanism Design

## Overview

The CrowdCode voting mechanism enables democratic decision-making for feature promotion while maintaining transparency, auditability, and minimal infrastructure requirements.

## Core Principles

1. **PatchPanel Exclusive**: Only authorized members can vote
2. **Transparent**: All votes are publicly visible
3. **Auditable**: Complete vote history in Git
4. **Simple**: Start with GitHub primitives
5. **Extensible**: Support future enhancements

## PatchPanel Membership

### Definition

**PatchPanel** is the group of users authorized to vote on feature promotion. The name evokes:
- A physical patch panel where connections are made
- Software patches being "patched in" to the codebase
- A panel of reviewers making decisions

### Membership Management

**Storage**: `.github/PATCHPANEL_MEMBERS.json`

```json
{
  "version": "1.0",
  "updated": "2025-12-21T21:00:00Z",
  "members": [
    {
      "github_username": "octocat",
      "joined": "2025-01-01T00:00:00Z",
      "physical_code": "PATCH-2025-0001",
      "role": "founding",
      "active": true
    },
    {
      "github_username": "mona",
      "joined": "2025-02-15T00:00:00Z",
      "physical_code": "PATCH-2025-0042",
      "role": "contributor",
      "active": true
    }
  ],
  "codes": {
    "prefix": "PATCH",
    "year": 2025,
    "next_sequence": 100,
    "redemption_enabled": true
  }
}
```

### Membership Roles

- **Founding**: Original project creators
- **Contributor**: Active code contributors
- **Community**: Physical code holders
- **Emeritus**: Inactive but retained membership

### Membership Acquisition

**Method 1: Physical Codes**
- Pre-generated unique codes (e.g., `PATCH-2025-0042`)
- Distributed at events, exhibitions, or collaborations
- Users redeem via GitHub issue with code
- Automated verification and membership grant

**Method 2: Contribution-Based**
- Automatic membership after N merged PRs
- Manual nomination by existing members
- Approval via vote from existing PatchPanel

**Method 3: Invitation-Only**
- Project maintainers invite specific users
- Immediate membership grant
- Audit trail in Git history

### Physical Code System

**Code Format**: `PATCH-YYYY-NNNN`
- `PATCH`: Platform identifier
- `YYYY`: Year of generation
- `NNNN`: Sequential number (0001-9999)

**Generation**:
```python
def generate_patch_code(year, sequence):
    """Generate unique PatchPanel code"""
    return f"PATCH-{year}-{sequence:04d}"

# Example
code = generate_patch_code(2025, 42)  # PATCH-2025-0042
```

**Redemption Flow**:
1. User creates issue with label `crowdcode:membership-request`
2. Issue body contains physical code
3. Workflow validates code is unused
4. Username added to PATCHPANEL_MEMBERS.json
5. Code marked as redeemed
6. User notified of membership

**Security**:
- Codes stored in encrypted secrets for validation
- One-time use only
- Expiration date (optional)
- Rate limiting on redemption attempts

## Voting Methods

### Phase 1: Reaction-Based Voting (MVP)

**Implementation**: GitHub PR reactions

**Vote Types**:
- 👍 (`:+1:`) = **Approve** - Ready to merge
- 👎 (`:-1:`) = **Reject** - Should not merge
- 👀 (`:eyes:`) = **Review Needed** - More discussion required

**Advantages**:
- Zero infrastructure required
- Built into GitHub UI
- Mobile-friendly
- Real-time visibility

**Limitations**:
- Single vote per user (can be changed)
- No delegation
- Limited vote types

**Vote Counting Algorithm**:
```python
def count_votes(pr_number, patchpanel_members):
    """Count votes from PatchPanel members only"""
    reactions = get_pr_reactions(pr_number)
    reviews = get_pr_reviews(pr_number)
    
    votes = {
        'approve': 0,
        'reject': 0,
        'review': 0,
        'total': 0
    }
    
    # Count reactions
    for reaction in reactions:
        if reaction.user.login in patchpanel_members:
            if reaction.content == '+1':
                votes['approve'] += 1
            elif reaction.content == '-1':
                votes['reject'] += 1
            elif reaction.content == 'eyes':
                votes['review'] += 1
            votes['total'] += 1
    
    # Count reviews (override reactions)
    review_votes = {}
    for review in reviews:
        if review.user.login in patchpanel_members:
            review_votes[review.user.login] = review.state
    
    for username, state in review_votes.items():
        if state == 'APPROVED':
            votes['approve'] += 1
        elif state == 'CHANGES_REQUESTED':
            votes['reject'] += 1
        elif state == 'COMMENTED':
            votes['review'] += 1
        votes['total'] += 1
    
    return votes
```

### Phase 2: Review-Based Voting

**Implementation**: GitHub PR reviews

**Vote Types**:
- **Approve** - Ready to merge
- **Request Changes** - Must address issues before merge
- **Comment** - Neutral feedback, not a blocking vote

**Advantages**:
- More formal than reactions
- Can include detailed feedback
- Built-in GitHub workflow
- Shows in PR status checks

**Limitations**:
- More friction than reactions
- Desktop-focused UI
- Can be intimidating for casual voters

**Hybrid Approach**:
- Accept both reactions AND reviews
- Reviews override reactions (more explicit)
- Simple majority from combined votes

### Phase 3: Advanced Voting (Future)

**Quadratic Voting**
- Each voter has vote credits (e.g., 100)
- Can allocate multiple credits to single vote
- Cost = credits²
- Example: 4 credits = 16 points

**Time-Weighted Voting**
- Earlier votes have more weight
- Encourages quick feedback
- Decay function: `weight = e^(-t/τ)`

**Reputation-Weighted Voting**
- Vote power based on contribution history
- Metrics: merged PRs, code quality, participation
- Prevents gaming through Sybil resistance

**Delegated Voting**
- Members can delegate votes to trusted members
- Useful for inactive periods
- Revocable at any time

## Promotion Criteria

### Minimal Viable Criteria

**Quorum**: Minimum number of votes required
```yaml
quorum: 3  # At least 3 PatchPanel members must vote
```

**Approval Threshold**: Percentage of approve votes
```yaml
approval_threshold: 0.5  # 50% of votes must be approve
```

**No Blocking Issues**: Critical concerns must be addressed
```yaml
blocking_labels:
  - "security-vulnerability"
  - "breaking-change-unreviewed"
  - "needs-major-refactor"
```

**Calculation**:
```python
def check_promotion_criteria(votes, config):
    """Determine if PR meets promotion criteria"""
    total_votes = votes['approve'] + votes['reject'] + votes['review']
    
    # Check quorum
    if total_votes < config.quorum:
        return False, f"Quorum not met ({total_votes}/{config.quorum})"
    
    # Check approval threshold
    approval_rate = votes['approve'] / total_votes
    if approval_rate < config.approval_threshold:
        return False, f"Approval rate too low ({approval_rate:.1%})"
    
    # Check blocking issues
    if has_blocking_labels(pr_number, config.blocking_labels):
        return False, "Blocking labels present"
    
    # Check security
    if has_security_vulnerabilities(pr_number):
        return False, "Security vulnerabilities detected"
    
    return True, "Ready to promote"
```

### Advanced Criteria (Future)

**Time-Based**:
- Minimum voting period (e.g., 7 days)
- Maximum staleness (e.g., 30 days)
- Automatic closure after timeout

**Quality-Based**:
- Code coverage threshold
- Linter pass required
- Performance benchmarks
- Documentation complete

**Community-Based**:
- Multiple vote rounds
- Supermajority for breaking changes (66%)
- Unanimous for architectural changes

## Vote Transparency

### Public Vote Display

**PR Description Update**:
```markdown
## 🗳️ PatchPanel Vote Status

**Vote Count**: 5 approve, 1 reject, 2 review (8 total)
**Approval Rate**: 62.5%
**Quorum**: ✅ Met (8/3)
**Status**: ✅ Ready to promote

### Votes by Member
- 👍 @octocat - "Love the dark mode!"
- 👍 @mona - "Well tested"
- 👍 @hubot - "Approved"
- 👍 @github - "Good work"
- 👍 @copilot - "AI approves"
- 👎 @reviewer - "Performance concerns" 
- 👀 @observer - "Need more testing"
- 👀 @watcher - "Looks promising"

### Promotion Decision
- **Date**: 2025-12-21
- **Decided By**: Automatic (threshold met)
- **Merged By**: github-actions[bot]
```

### Audit Trail

**Git History**:
- All vote updates committed
- Complete timeline of decisions
- Cryptographically signed commits

**Issue Timeline**:
- Vote events logged to linked issue
- Promotion decision documented
- Rejection reasoning captured

**Public Dashboard**:
```json
{
  "pr": 123,
  "feature": "dark-mode",
  "created": "2025-12-15T00:00:00Z",
  "voting_opened": "2025-12-15T01:00:00Z",
  "voting_closed": "2025-12-21T00:00:00Z",
  "votes": {
    "approve": 5,
    "reject": 1,
    "review": 2
  },
  "outcome": "promoted",
  "merged": "2025-12-21T00:30:00Z"
}
```

## Vote Security

### Sybil Resistance

**GitHub Authentication**:
- All votes tied to GitHub accounts
- GitHub's identity verification
- Public profile history

**PatchPanel Restriction**:
- Only pre-authorized members
- Membership changes auditable
- Prevents vote manipulation

### Vote Integrity

**Immutability**:
- Vote history in Git (cryptographic proof)
- PR reactions/reviews are timestamped
- Cannot retroactively change votes

**Audit**:
- Full vote history exportable
- Verification scripts available
- Transparent decision process

### Privacy Considerations

**Public by Default**:
- All votes are public
- Aligns with transparency goal
- Accountability for decisions

**Optional Anonymization** (Future):
- Anonymous vote casting
- Commitment scheme (hash then reveal)
- Zero-knowledge proofs for eligibility

## Voting UI/UX

### GitHub Web Interface

**For Voters**:
1. Navigate to PR
2. Click 👍 reaction (or write review)
3. Vote counted automatically
4. See live vote tally in PR description

**For Non-Members**:
1. Can see all votes
2. Can comment but not vote
3. Can request membership
4. Clear indication of vote eligibility

### GitHub Mobile App

- Full reaction support
- Review submission
- Vote tally visible
- Real-time updates

### Future Custom UI

**Vote Dashboard**:
- List of open votes
- Personalized vote queue
- Vote history
- Delegation management

**Notification System**:
- Email on new features
- Slack/Discord integration
- Vote reminders
- Outcome notifications

## Edge Cases

### Tie Votes
```python
if votes['approve'] == votes['reject']:
    # Default to not promoting (conservative)
    return False, "Tie vote - not promoting"
```

### Vote Changes
- Users can change reaction (last one counts)
- Reviews can be updated (last one counts)
- Vote history preserved in timeline

### Stale Votes
- Close voting after N days of inactivity
- Archive feature branch
- Allow reopening if interest resurges

### Controversial Features
- If >40% reject, trigger discussion period
- Require revision before re-voting
- May need supermajority (66%)

## Configuration

### Repository Settings

**`.github/crowdcode-config.yml`**:
```yaml
voting:
  # Quorum
  quorum: 3
  
  # Approval threshold
  approval_threshold: 0.5
  
  # Voting period
  voting_period_days: 7
  auto_close_stale: true
  
  # Vote sources
  count_reactions: true
  count_reviews: true
  
  # Valid reactions
  valid_reactions:
    approve: ["+1", "thumbsup", "heart"]
    reject: ["-1", "thumbsdown"]
    review: ["eyes", "thinking_face"]
  
  # Review states
  review_mapping:
    APPROVED: "approve"
    CHANGES_REQUESTED: "reject"
    COMMENTED: "review"
  
  # Supermajority requirements
  supermajority_labels:
    "breaking-change": 0.66
    "architecture-change": 0.80
  
  # Blocking conditions
  blocking_labels:
    - "security-vulnerability"
    - "needs-discussion"
```

## Migration Path

### Stage 1: Manual (Week 1-2)
- Reactions enabled
- Manual vote counting
- Manual promotion
- Learn usage patterns

### Stage 2: Semi-Automated (Week 3-4)
- Automated vote counting
- Manual promotion trigger
- Vote dashboard (static)
- Refine thresholds

### Stage 3: Fully Automated (Week 5+)
- Automatic promotion on threshold
- Real-time dashboard
- Notifications
- Advanced features

## Success Metrics

**Participation**:
- % of PatchPanel members voting
- Average time to vote
- Vote distribution (approve/reject/review)

**Quality**:
- % of promoted features still in main (6 months)
- Post-promotion issue rate
- Rollback frequency

**Efficiency**:
- Time from PR open to promotion
- Vote velocity (votes per day)
- Stale vote rate

## Best Practices

1. **Start Conservative**: High thresholds, lower later
2. **Encourage Participation**: Remind members to vote
3. **Make Voting Easy**: Reactions over reviews initially
4. **Be Transparent**: Public vote tallies
5. **Document Decisions**: Why features rejected/approved
6. **Iterate**: Adjust based on community feedback
7. **Respect Dissent**: Understand rejection reasons
8. **Celebrate Success**: Acknowledge promoted features

## Troubleshooting

**Low Participation**:
- Reduce quorum
- Send reminders
- Simplify voting (reactions)
- Highlight important votes

**Too Many Approvals**:
- Increase threshold
- Add quality checks
- Require tests/security scans
- Implement supermajority for risky changes

**Too Many Rejections**:
- Improve AI generation quality
- Better issue templates
- Pre-screening before PR
- Iterative refinement

**Gaming/Manipulation**:
- Review PatchPanel membership
- Audit vote patterns
- Implement rate limits
- Physical code requirement

## Future Enhancements

- **Smart Contracts**: Blockchain-based voting
- **Prediction Markets**: Bet on feature success
- **Liquid Democracy**: Delegated voting
- **Ranked Choice**: Multiple preference levels
- **Budget Voting**: Allocate resources across features
- **Futarchy**: Vote on values, bet on beliefs
- **Multi-Signature**: Require key stakeholder approval
- **Time Locks**: Delayed execution for critical changes
