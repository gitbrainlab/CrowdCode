#!/usr/bin/env python3
"""
CrowdCode: Validate and Count Votes from PatchPanel Members

This script counts votes (reactions and reviews) from authorized PatchPanel members
on AI-generated pull requests.
"""

import os
import sys
import json
import yaml
from github import Github
from datetime import datetime

def load_config():
    """Load CrowdCode configuration"""
    config_path = '.github/crowdcode-config.yml'
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Config file {config_path} not found, using defaults")
        return {
            'voting': {
                'quorum': 3,
                'approval_threshold': 0.5,
                'count_reactions': True,
                'count_reviews': True,
                'valid_reactions': {
                    'approve': ['+1', 'thumbsup'],
                    'reject': ['-1', 'thumbsdown'],
                    'review': ['eyes']
                }
            }
        }

def load_patchpanel_members():
    """Load PatchPanel member list"""
    members_path = '.github/PATCHPANEL_MEMBERS.json'
    try:
        with open(members_path, 'r') as f:
            data = json.load(f)
            return [m['github_username'] for m in data['members'] if m.get('active', True)]
    except FileNotFoundError:
        print(f"Warning: {members_path} not found, no authorized voters")
        return []

def count_votes(pr, members, config):
    """Count votes from PatchPanel members on a PR"""
    votes = {
        'approve': set(),
        'reject': set(),
        'review': set()
    }
    
    # Count reactions on PR body
    if config['voting'].get('count_reactions', True):
        try:
            # Get reactions on the PR itself
            for reaction in pr.get_reactions():
                if reaction.user.login in members:
                    content = reaction.content
                    if content in config['voting']['valid_reactions']['approve']:
                        votes['approve'].add(reaction.user.login)
                    elif content in config['voting']['valid_reactions']['reject']:
                        votes['reject'].add(reaction.user.login)
                    elif content in config['voting']['valid_reactions']['review']:
                        votes['review'].add(reaction.user.login)
        except Exception as e:
            print(f"    Warning: Could not fetch reactions: {e}")
    
    # Count reviews (these override reactions)
    if config['voting'].get('count_reviews', True):
        try:
            reviews = pr.get_reviews()
            review_votes = {}
            for review in reviews:
                if review.user.login in members:
                    # Last review from each user counts
                    review_votes[review.user.login] = review.state
            
            for username, state in review_votes.items():
                # Remove from other categories
                votes['approve'].discard(username)
                votes['reject'].discard(username)
                votes['review'].discard(username)
                
                # Add to appropriate category
                if state == 'APPROVED':
                    votes['approve'].add(username)
                elif state == 'CHANGES_REQUESTED':
                    votes['reject'].add(username)
                elif state == 'COMMENTED':
                    votes['review'].add(username)
        except Exception as e:
            print(f"    Warning: Could not fetch reviews: {e}")
    
    # Convert sets to counts
    return {
        'approve': len(votes['approve']),
        'reject': len(votes['reject']),
        'review': len(votes['review']),
        'total': len(votes['approve'] | votes['reject'] | votes['review']),
        'voters': {
            'approve': list(votes['approve']),
            'reject': list(votes['reject']),
            'review': list(votes['review'])
        }
    }

def check_promotion_criteria(votes, config):
    """Check if PR meets promotion criteria"""
    quorum = config['voting'].get('quorum', 3)
    threshold = config['voting'].get('approval_threshold', 0.5)
    
    total_votes = votes['total']
    
    if total_votes < quorum:
        return False, f"Quorum not met ({total_votes}/{quorum})"
    
    # Calculate approval rate from decisive votes only (exclude 'review')
    decisive_votes = votes['approve'] + votes['reject']
    if decisive_votes == 0:
        return False, "No decisive votes (only review votes)"
    
    approval_rate = votes['approve'] / decisive_votes
    
    if approval_rate < threshold:
        return False, f"Approval rate too low ({approval_rate:.1%} < {threshold:.0%})"
    
    return True, f"Ready to promote ({approval_rate:.1%} approval, {total_votes} votes)"

def generate_vote_summary(votes, ready, reason):
    """Generate markdown summary of votes"""
    decisive_votes = votes['approve'] + votes['reject']
    approval_pct = votes['approve'] / decisive_votes * 100 if decisive_votes > 0 else 0
    
    summary = f"""## 🗳️ PatchPanel Vote Status

**Vote Count**: {votes['approve']} approve, {votes['reject']} reject, {votes['review']} review ({votes['total']} total)
**Approval Rate**: {approval_pct:.1f}% ({votes['approve']}/{decisive_votes} decisive votes)
**Status**: {'✅ ' + reason if ready else '⏳ ' + reason}

### Votes by Member
"""
    
    if votes['voters']['approve']:
        summary += "\n**Approved** 👍:\n"
        for voter in votes['voters']['approve']:
            summary += f"- @{voter}\n"
    
    if votes['voters']['reject']:
        summary += "\n**Rejected** 👎:\n"
        for voter in votes['voters']['reject']:
            summary += f"- @{voter}\n"
    
    if votes['voters']['review']:
        summary += "\n**Review Needed** 👀:\n"
        for voter in votes['voters']['review']:
            summary += f"- @{voter}\n"
    
    summary += f"\n---\n*Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*"
    
    return summary

def main():
    """Main execution"""
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'
    
    if not github_token or not repo_name:
        print("Error: GITHUB_TOKEN and GITHUB_REPOSITORY must be set")
        sys.exit(1)
    
    print(f"CrowdCode Vote Counting")
    print(f"Repository: {repo_name}")
    print(f"Dry Run: {dry_run}")
    print("-" * 60)
    
    # Load configuration
    config = load_config()
    members = load_patchpanel_members()
    
    print(f"\nPatchPanel Members: {len(members)}")
    for member in members:
        print(f"  - {member}")
    
    if not members:
        print("\nWarning: No PatchPanel members configured!")
        print("Add members to .github/PATCHPANEL_MEMBERS.json")
    
    # Initialize GitHub client
    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    
    # Find PRs with voting label
    print(f"\nSearching for PRs with label 'crowdcode:voting'...")
    prs = repo.get_pulls(state='open')
    
    processed = 0
    for pr in prs:
        pr_labels = [label.name for label in pr.labels]
        
        if 'crowdcode:voting' not in pr_labels and 'crowdcode:ai-generated' not in pr_labels:
            continue
        
        print(f"\nProcessing PR #{pr.number}: {pr.title}")
        
        # Count votes
        votes = count_votes(pr, members, config)
        print(f"  Votes: {votes['approve']} approve, {votes['reject']} reject, {votes['review']} review")
        
        # Check promotion criteria
        ready, reason = check_promotion_criteria(votes, config)
        print(f"  Status: {reason}")
        
        # Generate summary
        summary = generate_vote_summary(votes, ready, reason)
        
        if not dry_run:
            try:
                # Update PR body with vote summary
                # Find existing vote summary and replace it
                body = pr.body or ""
                if "## 🗳️ PatchPanel Vote Status" in body:
                    # Replace existing summary
                    parts = body.split("## 🗳️ PatchPanel Vote Status")
                    # Find the end of the vote summary (next ## or end of string)
                    summary_end = parts[1].find("\n## ")
                    if summary_end == -1:
                        summary_end = parts[1].find("\n---\n**Related Issue**")
                    if summary_end != -1:
                        new_body = parts[0] + summary + parts[1][summary_end:]
                    else:
                        new_body = parts[0] + summary
                else:
                    # Add summary before related issue footer
                    if "**Related Issue**" in body:
                        parts = body.split("---\n**Related Issue**")
                        new_body = parts[0] + summary + "\n\n---\n**Related Issue**" + parts[1]
                    else:
                        new_body = body + "\n\n" + summary
                
                pr.edit(body=new_body)
                
                # Update labels
                current_labels = [label.name for label in pr.labels]
                if ready and 'crowdcode:ready-to-promote' not in current_labels:
                    pr.add_to_labels('crowdcode:ready-to-promote')
                    print(f"  ✓ Added 'crowdcode:ready-to-promote' label")
                
                print(f"  ✓ Updated PR description with vote summary")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print(f"  [DRY RUN] Would update PR description")
            if ready:
                print(f"  [DRY RUN] Would add 'crowdcode:ready-to-promote' label")
        
        processed += 1
    
    print(f"\n{'=' * 60}")
    print(f"Processed {processed} PR(s)")
    print("Complete!")

if __name__ == '__main__':
    main()
