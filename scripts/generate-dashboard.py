#!/usr/bin/env python3
"""
CrowdCode: Generate Feature Dashboard

This script generates a dashboard showing all CrowdCode features across branches.
"""

import os
import sys
import json
from github import Github
from datetime import datetime

def main():
    """Main execution"""
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    
    if not github_token or not repo_name:
        print("Error: GITHUB_TOKEN and GITHUB_REPOSITORY must be set")
        sys.exit(1)
    
    print(f"CrowdCode Feature Dashboard Generator")
    print(f"Repository: {repo_name}")
    print("-" * 60)
    
    # Initialize GitHub client
    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    
    # Collect feature data
    features = []
    
    # Get all feature branches
    branches = repo.get_branches()
    for branch in branches:
        if branch.name.startswith('crowdcode/feature-'):
            # Parse branch name
            parts = branch.name.split('-')
            if len(parts) >= 3:
                try:
                    issue_num = int(parts[2])
                    features.append({
                        'branch': branch.name,
                        'issue': issue_num,
                        'status': 'branch-only'
                    })
                except ValueError:
                    pass
    
    # Get all PRs
    prs = repo.get_pulls(state='all')
    for pr in prs:
        pr_labels = [label.name for label in pr.labels]
        
        if any(label.startswith('crowdcode:') for label in pr_labels):
            # Determine status
            if 'crowdcode:promoted' in pr_labels:
                status = 'promoted'
            elif 'crowdcode:ready-to-promote' in pr_labels:
                status = 'ready-to-promote'
            elif 'crowdcode:voting' in pr_labels or 'crowdcode:ai-generated' in pr_labels:
                status = 'voting'
            elif 'crowdcode:pending-pr' in pr_labels:
                status = 'pending'
            elif 'crowdcode:archived' in pr_labels:
                status = 'archived'
            else:
                status = 'unknown'
            
            features.append({
                'branch': pr.head.ref if pr.head else 'unknown',
                'issue': pr.number,
                'pr': pr.number,
                'status': status,
                'created': pr.created_at.isoformat(),
                'title': pr.title,
                'description': pr.title
            })
    
    # Generate dashboard data
    dashboard = {
        'generated': datetime.utcnow().isoformat(),
        'repository': repo_name,
        'features': features,
        'statistics': {
            'total_features': len(features),
            'promoted': len([f for f in features if f.get('status') == 'promoted']),
            'voting': len([f for f in features if f.get('status') == 'voting']),
            'pending': len([f for f in features if f.get('status') == 'pending']),
            'archived': len([f for f in features if f.get('status') == 'archived'])
        }
    }
    
    # Write dashboard JSON
    os.makedirs('docs/features', exist_ok=True)
    with open('docs/features/index.json', 'w') as f:
        json.dump(dashboard, f, indent=2)
    
    print(f"\n✓ Generated dashboard with {len(features)} features")
    print(f"  - Promoted: {dashboard['statistics']['promoted']}")
    print(f"  - Voting: {dashboard['statistics']['voting']}")
    print(f"  - Pending: {dashboard['statistics']['pending']}")
    print(f"  - Archived: {dashboard['statistics']['archived']}")
    
    # Generate README
    readme = f"""# CrowdCode Features

**Last Updated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

## Statistics

- **Total Features**: {dashboard['statistics']['total_features']}
- **Promoted**: {dashboard['statistics']['promoted']}
- **Voting**: {dashboard['statistics']['voting']}
- **Pending**: {dashboard['statistics']['pending']}
- **Archived**: {dashboard['statistics']['archived']}

## All Features

"""
    
    for feature in sorted(features, key=lambda f: f.get('created', ''), reverse=True):
        status_emoji = {
            'promoted': '✅',
            'ready-to-promote': '🎯',
            'voting': '🗳️',
            'pending': '⏳',
            'archived': '📦',
            'branch-only': '🌿'
        }.get(feature.get('status', 'unknown'), '❓')
        
        title = feature.get('title', feature.get('branch', 'Unknown'))
        issue_num = feature.get('issue', '')
        pr_num = feature.get('pr', '')
        
        readme += f"- {status_emoji} **{title}**"
        if issue_num:
            readme += f" ([Issue #{issue_num}](../../issues/{issue_num}))"
        if pr_num:
            readme += f" ([PR #{pr_num}](../../pull/{pr_num}))"
        readme += f" - {feature.get('status', 'unknown')}\n"
    
    with open('docs/features/README.md', 'w') as f:
        f.write(readme)
    
    print("✓ Generated README.md")
    print("\nComplete!")

if __name__ == '__main__':
    main()
