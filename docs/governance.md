# CrowdCode Governance

> **Democratic decision-making for feature promotion**

This document describes how CrowdCode's voting system works, how PatchPanel membership is managed, and how to resolve conflicts in voting.

## Overview

CrowdCode uses a **democratic voting system** where authorized members (the "PatchPanel") vote on whether AI-generated features should be promoted to the main branch.

**Key Principles**:
- 🗳️ **Democratic**: One member, one vote (by default)
- 🔒 **Restricted**: Only PatchPanel members can vote
- 👁️ **Transparent**: All votes are publicly visible
- 📊 **Threshold-based**: Features promoted when quorum + approval met
- ⚖️ **Fair**: Clear rules for conflict resolution

---

## PatchPanel Membership

### What is PatchPanel?

**PatchPanel** is the authorized group of voters who decide which features get promoted. The name evokes:
- A physical patch panel where connections are made
- Software patches being "patched in" to the codebase
- A panel of reviewers making decisions

### Membership Storage

Members are defined in `.github/PATCHPANEL_MEMBERS.json`:

```json
{
  "version": "1.0",
  "updated": "2025-12-29T00:00:00Z",
  "description": "Authorized PatchPanel members for CrowdCode voting",
  "members": [
    {
      "github_username": "alice",
      "joined": "2025-01-15T00:00:00Z",
      "role": "founding",
      "active": true,
      "notes": "Project founder"
    },
    {
      "github_username": "bob",
      "joined": "2025-03-20T00:00:00Z",
      "role": "contributor",
      "active": true,
      "notes": "Core contributor, 50+ merged PRs"
    },
    {
      "github_username": "charlie",
      "joined": "2025-06-10T00:00:00Z",
      "role": "community",
      "active": true,
      "notes": "Redeemed physical code PATCH-2025-0042"
    },
    {
      "github_username": "diana",
      "joined": "2024-01-01T00:00:00Z",
      "role": "emeritus",
      "active": false,
      "notes": "Founding member, now inactive"
    }
  ],
  "codes": {
    "prefix": "PATCH",
    "year": 2025,
    "next_sequence": 100,
    "redemption_enabled": false
  }
}
```

### Member Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `github_username` | string | ✅ Yes | Exact GitHub username (case-sensitive) |
| `joined` | ISO 8601 | ✅ Yes | Membership start date |
| `role` | string | ✅ Yes | Member type: `founding`, `contributor`, `community`, `emeritus` |
| `active` | boolean | ✅ Yes | `true` = votes count, `false` = votes ignored |
| `notes` | string | ❌ No | Optional description/context |

**⚠️ Critical**: Only members with `"active": true` can vote.

### Membership Roles

| Role | Description | Typical Acquisition |
|------|-------------|---------------------|
| **Founding** | Original project creators | Invited by repository owner |
| **Contributor** | Active code contributors | Automatic after N merged PRs OR manual invitation |
| **Community** | Physical code holders | Redeemed code at event/exhibition |
| **Emeritus** | Inactive but retained membership | Previous members who stepped down |

**Note**: Roles are informational only. All `active: true` members have equal voting power (by default).

### Adding Members

#### Method 1: Direct Addition (Immediate)

Edit `.github/PATCHPANEL_MEMBERS.json` and commit:

```bash
# Edit membership file
vim .github/PATCHPANEL_MEMBERS.json

# Add new member to "members" array:
{
  "github_username": "newmember",
  "joined": "2025-12-29T15:00:00Z",
  "role": "contributor",
  "active": true,
  "notes": "Added for valuable contributions"
}

# Commit and push
git add .github/PATCHPANEL_MEMBERS.json
git commit -m "Add @newmember to PatchPanel"
git push
```

**⚠️ Security**: Only repository maintainers should have permission to edit this file.

#### Method 2: Physical Code Redemption (Future Feature)

Enable code redemption in config:

```json
{
  "codes": {
    "prefix": "PATCH",
    "year": 2025,
    "next_sequence": 100,
    "redemption_enabled": true  // Enable code redemption
  }
}
```

Users redeem codes via GitHub issue:
1. Create issue with label `crowdcode:membership-request`
2. Provide code: `PATCH-2025-0042`
3. Automated workflow validates code
4. If valid, adds member to file
5. Closes issue with welcome message

**Code format**: `PATCH-YYYY-NNNN`
- `PATCH`: Platform identifier
- `YYYY`: Year of generation (e.g., 2025)
- `NNNN`: Sequential number (e.g., 0042)

**Example**: `PATCH-2025-0042` is the 42nd code generated in 2025.

#### Method 3: Contribution-Based (Automated - Future)

Automatic membership after contributions:

```yaml
# In .github/crowdcode-config.yml (future feature)
patchpanel:
  auto_add_contributors:
    enabled: false  # Not yet implemented
    merged_pr_threshold: 10  # After 10 merged PRs
    role: "contributor"
```

### Removing Members

#### Soft Removal (Recommended)

Set `active: false` to preserve history:

```json
{
  "github_username": "oldmember",
  "joined": "2024-01-01T00:00:00Z",
  "role": "emeritus",  // Change role
  "active": false,     // Disable voting
  "notes": "Stepped down on 2025-12-29"
}
```

**Advantage**: Preserves audit trail of historical votes.

#### Hard Removal (Not Recommended)

Delete member from array:

```bash
# Remove member from JSON
vim .github/PATCHPANEL_MEMBERS.json
# Delete entire member object

git add .github/PATCHPANEL_MEMBERS.json
git commit -m "Remove @oldmember from PatchPanel"
git push
```

**⚠️ Warning**: Historical votes may become invalid.

---

## Voting Mechanism

### How Votes are Cast

PatchPanel members can vote using two methods:

#### Method 1: Emoji Reactions (Simple)

React to the PR description with emojis:

| Emoji | Reaction Code | Meaning | Effect |
|-------|---------------|---------|--------|
| 👍 | `:+1:`, `:thumbsup:`, `:heart:` | **Approve** | Counts as approval |
| 👎 | `:-1:`, `:thumbsdown:` | **Reject** | Counts as rejection |
| 👀 | `:eyes:`, `:thinking_face:` | **Need Review** | Neutral, doesn't count toward approval |

**How to react**:
1. Go to the Pull Request
2. Find the PR description (first comment)
3. Click the emoji button
4. Select 👍, 👎, or 👀

**Advantages**:
- ✅ Fast and easy
- ✅ No GitHub review workflow needed
- ✅ Visible to all users

**Disadvantages**:
- ❌ Less formal than reviews
- ❌ No space for detailed feedback

#### Method 2: Pull Request Reviews (Formal)

Submit a formal GitHub PR review:

| Review Type | Meaning | Effect |
|-------------|---------|--------|
| **Approve** | Strong support, ready to merge | Counts as approval |
| **Request Changes** | Blocking concerns, needs work | Counts as rejection |
| **Comment** | Feedback without blocking | Neutral (like 👀) |

**How to review**:
1. Go to the Pull Request
2. Click "Files changed" tab
3. Review the code
4. Click "Review changes" button
5. Select review type and submit

**Advantages**:
- ✅ More formal and professional
- ✅ Can leave inline code comments
- ✅ Weighted more heavily (optional)

**Disadvantages**:
- ❌ More time-consuming
- ❌ Requires understanding PR review UI

### Vote Counting Rules

Votes are counted and updated hourly by the Vote Counting workflow.

#### Basic Counting

1. **Load PatchPanel members** from `.github/PATCHPANEL_MEMBERS.json`
2. **Filter to active members** (`active: true`)
3. **For each PR labeled `crowdcode:voting`**:
   - Fetch all reactions on PR description
   - Fetch all PR reviews
   - Filter to only PatchPanel members
   - Map reactions/reviews to vote types:
     ```
     Approve = (👍 reactions) + (Approved reviews)
     Reject = (👎 reactions) + (Request Changes reviews)
     Review = (👀 reactions) + (Comment reviews)
     ```
4. **Calculate vote tally**:
   - Total votes = Approve + Reject + Review
   - Approval rate = Approve / (Approve + Reject)
   - Note: "Review" votes don't count toward approval rate

#### Configuration

```yaml
# In .github/crowdcode-config.yml
voting:
  quorum: 3  # Minimum votes required
  approval_threshold: 0.5  # 50% approval (0.0 to 1.0)
  voting_period_days: 7  # How long voting stays open
  auto_close_on_threshold: true  # Close when threshold met
  count_reactions: true  # Count emoji reactions
  count_reviews: true    # Count PR reviews
```

#### Vote Thresholds

A feature is **ready to promote** when:

```
(Approve + Reject) >= quorum
AND
(Approve / (Approve + Reject)) >= approval_threshold
```

**Example scenarios**:

| Approve | Reject | Review | Total | Rate | Quorum (3) | Threshold (50%) | Ready? |
|---------|--------|--------|-------|------|------------|-----------------|--------|
| 5 | 1 | 2 | 8 | 83% | ✅ Yes | ✅ Yes | ✅ **YES** |
| 3 | 2 | 0 | 5 | 60% | ✅ Yes | ✅ Yes | ✅ **YES** |
| 2 | 1 | 0 | 3 | 67% | ✅ Yes | ✅ Yes | ✅ **YES** |
| 2 | 0 | 1 | 3 | 100% | ❌ No (only 2 A+R) | ✅ Yes | ❌ **NO** (quorum) |
| 1 | 2 | 0 | 3 | 33% | ✅ Yes | ❌ No | ❌ **NO** (threshold) |
| 5 | 5 | 0 | 10 | 50% | ✅ Yes | ✅ Yes (exactly 50%) | ✅ **YES** |

**Note**: "Review" votes (👀) don't count toward quorum or threshold. They indicate "needs more time" without blocking.

### Vote Weight (Future Enhancement)

Currently, all PatchPanel members have equal voting power (1 vote each).

**Future enhancement**: Weighted voting based on role or contribution:

```yaml
# Future configuration (not yet implemented)
voting:
  weighted_voting:
    enabled: false
    weights:
      founding: 2.0
      contributor: 1.5
      community: 1.0
      emeritus: 0.0
```

### Voting Period

Features have a voting window:

```yaml
voting:
  voting_period_days: 7  # Default: 7 days
```

**What happens after voting period expires?**

**Option 1**: Auto-close if threshold not met
```yaml
voting:
  auto_close_on_threshold: true  # Close voting when period expires
```
- PR labeled `crowdcode:archived`
- Issue closed with rejection comment
- Branch preserved for transparency

**Option 2**: Keep voting open indefinitely
```yaml
voting:
  auto_close_on_threshold: false  # Keep voting open
```
- PR remains in voting state
- Can still reach threshold later

**Recommendation**: Use `auto_close_on_threshold: true` to prevent stale votes.

---

## Conflict Resolution

### Scenario 1: Tied Votes

**Problem**: Equal approve and reject votes (e.g., 3 approve, 3 reject)

**Resolution strategy**:

1. **Check threshold**: With `approval_threshold: 0.5`, exactly 50% meets threshold
   - 3 approve / 6 total = 50% → **APPROVED** ✅

2. **Require majority**: Change to `approval_threshold: 0.51` to require >50%
   - 3 approve / 6 total = 50% → **REJECTED** ❌

**Configuration**:
```yaml
voting:
  approval_threshold: 0.5   # Exactly 50% passes (ties approve)
  # OR
  approval_threshold: 0.51  # More than 50% required (ties reject)
```

**Recommendation**: Use `0.5` to give benefit of doubt to proposals.

### Scenario 2: Quorum Not Met

**Problem**: Not enough votes (e.g., 2 votes but quorum is 3)

**Resolution options**:

**Option A**: Wait for more votes
- Keep PR labeled `crowdcode:voting`
- Encourage members to vote
- Extend voting period if needed

**Option B**: Lower quorum
```yaml
voting:
  quorum: 2  # Reduce from 3 to 2
```

**Option C**: Close as rejected after voting period
```yaml
voting:
  voting_period_days: 7
  auto_close_on_threshold: true  # Auto-reject if quorum not met
```

**Recommendation**: For small teams (<5 members), set `quorum: 2`.

### Scenario 3: Vote Changes

**Problem**: Member changes vote (reaction → review, or changes review type)

**Resolution**: Use most recent vote
- Vote counting workflow uses latest state
- Reactions can be added/removed
- Reviews can be dismissed and re-submitted
- Latest state wins

**Example**:
1. Alice adds 👍 reaction (approve)
2. Vote count: 1 approve
3. Alice removes 👍, submits "Request Changes" review (reject)
4. Vote count: 0 approve, 1 reject

**Note**: Vote history is preserved in GitHub audit log.

### Scenario 4: Member Deactivated Mid-Vote

**Problem**: Member votes, then is set to `active: false`

**Resolution**: Votes from inactive members are ignored
- Vote counting workflow re-runs hourly
- Only counts votes from `active: true` members
- Deactivating member instantly removes their vote

**Example**:
1. Bob votes 👍 (active: true)
2. Vote count: 1 approve
3. Bob set to `active: false`
4. Vote count: 0 approve (Bob's vote no longer counts)

**⚠️ Warning**: Use carefully, as it retroactively changes vote tallies.

### Scenario 5: Conflicting Votes (Reaction + Review)

**Problem**: Member adds both 👍 reaction AND "Request Changes" review

**Resolution**: Reviews override reactions
- PR reviews are more formal than reactions
- Latest review state takes precedence
- If member has both 👍 reaction and "Approved" review, counts as 1 approve (not 2)

**Priority order** (highest to lowest):
1. Most recent PR review (Approved > Request Changes > Comment)
2. Emoji reactions (if no review)

**Example**:
- Alice adds 👍 reaction
- Later, Alice submits "Approved" review
- **Result**: 1 approve vote (review overrides reaction)

### Scenario 6: Vote Manipulation Attempt

**Problem**: User creates fake accounts to vote

**Detection**:
- Only votes from members in `PATCHPANEL_MEMBERS.json` count
- Membership file is version-controlled (audit trail)
- GitHub accounts have creation dates visible

**Prevention**:
- ✅ Restrict PatchPanel to known, trusted members
- ✅ Require membership justification in `notes` field
- ✅ Review membership file changes in PRs
- ✅ Monitor for suspicious voting patterns

**Response**:
1. Remove fake accounts from membership file
2. Re-run vote counting workflow
3. Investigate how accounts were added
4. Strengthen membership approval process

---

## Best Practices

### For Voters

1. **Vote Promptly**: Review PRs within the voting period (default: 7 days)
2. **Provide Feedback**: Comment on why you approve/reject
3. **Test the Code**: Try out features before voting when possible
4. **Be Constructive**: If rejecting, explain concerns
5. **Stay Active**: Participate regularly in voting
6. **Update Votes**: Change your vote if new information emerges

### For Maintainers

1. **Start Small**: Begin with 2-3 trusted PatchPanel members
2. **Document Membership**: Use `notes` field to explain why members were added
3. **Review Regularly**: Audit membership quarterly
4. **Communicate Changes**: Notify members when thresholds change
5. **Preserve History**: Use `active: false` instead of deleting members
6. **Monitor Voting**: Check for stalled votes and low participation

### For Feature Requesters

1. **Be Patient**: Voting takes time (7 days default)
2. **Engage**: Respond to questions and feedback
3. **Improve Proposals**: Update feature requests based on concerns
4. **Respect Decisions**: Understand that rejection is possible
5. **Learn**: Use rejected features to improve future proposals

---

## Voting Metrics

### Participation Rate

Monitor how many PatchPanel members vote:

```
Participation Rate = (Unique Voters / Active Members) × 100%
```

**Example**:
- 5 active PatchPanel members
- 4 voted on PR #42
- Participation: 4/5 = 80%

**Target**: >70% participation for healthy governance.

### Approval Rate

Track overall community sentiment:

```
Approval Rate = (Approved Features / Total Features) × 100%
```

**Example**:
- 10 features reached voting
- 7 approved, 3 rejected
- Approval rate: 7/10 = 70%

**Interpretation**:
- <40%: Community is very selective (high bar)
- 40-70%: Healthy balance
- >70%: Community approves most features (low bar)

### Time to Decision

Average time from PR creation to promotion/rejection:

```
Average Decision Time = Σ(Decision Date - PR Date) / Total Features
```

**Target**: <7 days (within one voting period).

---

## Configuration Examples

### Conservative (High Bar)

For critical projects requiring consensus:

```yaml
voting:
  quorum: 5              # Need many voters
  approval_threshold: 0.7  # 70% approval required
  voting_period_days: 14   # Longer voting window
```

### Balanced (Recommended)

For most projects:

```yaml
voting:
  quorum: 3              # Reasonable minimum
  approval_threshold: 0.5  # Simple majority
  voting_period_days: 7    # One week
```

### Progressive (Low Bar)

For experimental projects encouraging features:

```yaml
voting:
  quorum: 2              # Only need a few votes
  approval_threshold: 0.4  # 40% approval (minority can approve)
  voting_period_days: 3    # Quick decisions
```

### Small Team (2-5 members)

```yaml
voting:
  quorum: 2              # At least 2 votes
  approval_threshold: 0.5  # Simple majority
  voting_period_days: 5    # Shorter window
```

### Large Team (20+ members)

```yaml
voting:
  quorum: 7              # More voices required
  approval_threshold: 0.6  # 60% approval
  voting_period_days: 10   # Longer for coordination
```

---

## Audit and Transparency

### Vote History

All votes are publicly visible:
- Reactions on PR descriptions (visible to all)
- PR reviews (visible to all)
- Vote tallies in PR descriptions (updated hourly)

**Audit trail**:
- Git history of `PATCHPANEL_MEMBERS.json` (who was eligible)
- GitHub PR/issue timeline (when votes were cast)
- Workflow run logs (vote counting results)

### Membership Changes

Track membership changes via Git:

```bash
# View membership history
git log -p .github/PATCHPANEL_MEMBERS.json

# See who was added/removed when
git blame .github/PATCHPANEL_MEMBERS.json
```

### Voting Transparency

Display vote status prominently on PRs:

```markdown
## 🗳️ PatchPanel Vote Status

**Votes**: 8 total
- ✅ Approve: 6 (75%)
- ❌ Reject: 2 (25%)
- 👀 Review: 0

**Quorum**: 3 required, 8 voting → ✅ Met
**Threshold**: 50% required, 75% approval → ✅ Met

**Status**: ✅ Ready to promote

**Voters**:
- @alice: ✅ Approved (review)
- @bob: ✅ Approved (👍)
- @charlie: ❌ Rejected (review)
- @diana: ✅ Approved (👍)
- @eve: ✅ Approved (👍)
- @frank: ✅ Approved (review)
- @grace: ✅ Approved (👍)
- @henry: ❌ Rejected (👎)
```

---

## Governance Evolution

### Phase 1: Manual Governance (Current)

- Manual PatchPanel membership management
- Simple majority voting
- Equal vote weights

### Phase 2: Semi-Automated (Future)

- Contribution-based auto-membership
- Weighted voting by role
- Physical code redemption

### Phase 3: Advanced Governance (Future)

- Reputation-based voting weights
- Quadratic voting
- Delegation/proxy voting
- Liquid democracy

---

## Next Steps

1. ✅ Understand voting mechanism
2. 📖 Read [Threat Model](threat-model.md) for security considerations
3. ⚙️ Configure voting thresholds for your project
4. 👥 Define initial PatchPanel members
5. 🚀 Start using democratic feature promotion!

---

**Need help?** See [Setup Guide](setup.md) or [Documentation Index](index.md).
