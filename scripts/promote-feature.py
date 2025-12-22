#!/usr/bin/env python3
"""
CrowdCode: Promote Approved Features to Main Branch

This script merges approved pull requests to the main branch based on
PatchPanel votes meeting the promotion threshold.
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
            'promotion': {
                'merge_method': 'squash',
                'require_tests': False,
                'require_codeql': False,
                'auto_delete_branch': False,
                'notify_members': True
            }
        }

def main():
    """Main execution"""
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'
    
    if not github_token or not repo_name:
        print("Error: GITHUB_TOKEN and GITHUB_REPOSITORY must be set")
        sys.exit(1)
    
    print(f"CrowdCode Feature Promotion")
    print(f"Repository: {repo_name}")
    print(f"Dry Run: {dry_run}")
    print("-" * 60)
    
    # Load configuration
    config = load_config()
    merge_method = config['promotion'].get('merge_method', 'squash')
    
    # Initialize GitHub client
    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    
    # Find PRs ready to promote
    print(f"\nSearching for PRs with label 'crowdcode:ready-to-promote'...")
    prs = repo.get_pulls(state='open')
    
    promoted = 0
    for pr in prs:
        pr_labels = [label.name for label in pr.labels]
        
        if 'crowdcode:ready-to-promote' not in pr_labels:
            continue
        
        print(f"\nProcessing PR #{pr.number}: {pr.title}")
        
        # Check if PR is mergeable
        if not pr.mergeable:
            print(f"  ⚠️  PR has merge conflicts, skipping")
            continue
        
        # Check status checks if required
        if config['promotion'].get('require_tests', False):
            # Would check CI status here
            print(f"  ⚠️  Test requirement checking not yet implemented")
        
        if config['promotion'].get('require_codeql', False):
            # Would check CodeQL status here
            print(f"  ⚠️  CodeQL requirement checking not yet implemented")
        
        if not dry_run:
            try:
                # For now, just update labels to show it would be promoted
                # Full merge implementation will come once we have actual PRs with code
                pr.remove_from_labels('crowdcode:ready-to-promote')
                pr.add_to_labels('crowdcode:promoted')
                
                # Add comment
                pr.create_comment(
                    f"🎉 **Feature Promoted!**\n\n"
                    f"This feature has been approved by the PatchPanel and is ready for merge.\n\n"
                    f"**Note**: Actual merge to main will be implemented in Phase 2 once we have "
                    f"AI-generated code to merge. For now, this demonstrates the promotion workflow."
                )
                
                # Close linked issue
                # Parse issue number from PR body
                if pr.body and "**Related Issue**: #" in pr.body:
                    issue_num_str = pr.body.split("**Related Issue**: #")[1].split()[0]
                    try:
                        issue_num = int(issue_num_str)
                        issue = repo.get_issue(issue_num)
                        issue.create_comment(
                            f"✅ **Feature Promoted!**\n\n"
                            f"This feature request has been approved and promoted via PR #{pr.number}.\n\n"
                            f"Thank you for your contribution to the project!"
                        )
                        issue.add_to_labels('crowdcode:promoted')
                        issue.edit(state='closed')
                        print(f"  ✓ Closed issue #{issue_num}")
                    except (ValueError, IndexError) as e:
                        print(f"  ⚠️  Could not parse issue number: {e}")
                
                print(f"  ✓ Updated labels to 'crowdcode:promoted'")
                print(f"  ✓ Posted promotion comment")
                promoted += 1
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print(f"  [DRY RUN] Would merge PR using method: {merge_method}")
            print(f"  [DRY RUN] Would update labels to 'crowdcode:promoted'")
            print(f"  [DRY RUN] Would close linked issue")
            promoted += 1
    
    print(f"\n{'=' * 60}")
    print(f"Promoted {promoted} feature(s)")
    print("Complete!")

if __name__ == '__main__':
    main()
