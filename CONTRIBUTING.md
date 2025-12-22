# Contributing to CrowdCode

Thank you for your interest in contributing to CrowdCode! This document explains how to contribute to the project.

## How CrowdCode Works

CrowdCode is a meta project - it uses itself for development! This means:

1. **Feature Requests**: Submit via [GitHub Issues](../../issues/new?template=feature-request.yml)
2. **AI Generation**: GitHub Actions generates PRs automatically
3. **Community Voting**: PatchPanel members vote on features
4. **Automatic Promotion**: Approved features are merged to main

## Ways to Contribute

### 💡 Submit Feature Ideas

The primary way to contribute is by submitting feature requests:

1. Go to [Issues](../../issues/new?template=feature-request.yml)
2. Select "CrowdCode Feature Request"
3. Fill out the template completely:
   - **Feature Name**: Concise, descriptive title
   - **Description**: What should it do?
   - **Use Case**: Why is it valuable?
   - **Acceptance Criteria**: How to verify it works?

**Tips for good feature requests**:
- Be specific and detailed
- Explain the "why" not just the "what"
- Provide examples or references
- Consider edge cases
- Define success criteria

### 🗳️ Join the PatchPanel

PatchPanel members vote on which features to promote:

**To request membership**:
1. Open an issue requesting PatchPanel membership
2. Explain why you'd like to participate
3. Describe your interest in the project
4. Wait for review by existing members

**Responsibilities**:
- Review AI-generated PRs thoughtfully
- Vote on features (approve, reject, or request review)
- Provide constructive feedback
- Participate regularly (at least monthly)

### 🐛 Report Bugs

Found a bug? Let us know:

1. Check if it's already reported in [Issues](../../issues)
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, browser, etc.)
   - Screenshots if applicable

### 📖 Improve Documentation

Documentation improvements are always welcome:

1. Submit a feature request for documentation changes
2. Or submit a direct pull request for:
   - Typo fixes
   - Clarifications
   - Examples
   - Formatting improvements

### 💻 Submit Pull Requests

While CrowdCode uses AI for feature implementation, you can still submit PRs for:

- **Urgent bug fixes**: Critical issues needing immediate attention
- **Documentation**: Improvements to markdown files
- **Small improvements**: Minor tweaks and optimizations

**PR Guidelines**:
1. Keep changes focused and minimal
2. Follow existing code style
3. Update documentation if needed
4. Add tests if applicable
5. Reference related issues

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- GitHub CLI (optional, recommended)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/evcatalyst/CrowdCode.git
cd CrowdCode

# Install dependencies
pip install -r requirements.txt

# Run tests (when available)
python -m pytest
```

### Testing Workflows Locally

Use [act](https://github.com/nektos/act) to test GitHub Actions locally:

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Test a workflow
act -j generate-prs -s GITHUB_TOKEN=your_token
```

### Dry-Run Mode

All scripts support dry-run mode for testing:

```bash
# Test PR generation without making changes
python scripts/generate-feature-pr.py
export DRY_RUN=true

# Test vote counting
python scripts/validate-votes.py
```

## Code Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use type hints where appropriate
- Add docstrings for functions
- Keep functions focused and small

### Documentation

- Use Markdown for all documentation
- Include code examples
- Add links to related documents
- Keep README.md up to date

### Git Commits

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep commits focused on single changes
- Reference issues when applicable

**Example**:
```
Add vote notification feature

Implements email notifications when features are promoted.
Closes #42
```

## Voting Guidelines

### For PatchPanel Members

When voting on features:

**Approve (👍) when**:
- Implementation matches requirements
- Code quality is acceptable
- No security concerns
- Aligns with project goals
- Tests pass (when required)

**Reject (👎) when**:
- Implementation is incomplete
- Security vulnerabilities present
- Breaking changes without discussion
- Doesn't match requirements
- Quality issues

**Request Review (👀) when**:
- Need more time to evaluate
- Want other opinions
- Implementation looks promising but needs refinement
- Unclear about requirements

**Best Practices**:
- Review thoroughly before voting
- Provide constructive feedback
- Explain rejection reasons
- Test the implementation when possible
- Vote within the voting period

## Community Guidelines

### Code of Conduct

We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/):

- **Be respectful**: Treat everyone with respect
- **Be inclusive**: Welcome diverse perspectives
- **Be constructive**: Focus on issues, not people
- **Be collaborative**: Work together toward shared goals

### Communication

- **Issues**: For feature requests and bugs
- **Discussions**: For questions and ideas (coming soon)
- **Pull Requests**: For code contributions
- **Email**: For sensitive matters

### Decision Making

CrowdCode uses democratic decision-making:

1. **Proposals**: Anyone can propose features
2. **Discussion**: Community discusses merits
3. **Implementation**: AI generates initial code
4. **Voting**: PatchPanel votes on promotion
5. **Promotion**: Approved features merge to main

## Release Process

Releases are created automatically when:
- Significant features are promoted
- Major milestones are reached
- Monthly release cycles (future)

## Getting Help

- 📖 Read the [documentation](docs/)
- 🐛 Check [existing issues](../../issues)
- 💬 Start a [discussion](../../discussions) (coming soon)
- 📧 Contact maintainers

## Recognition

Contributors are recognized through:
- GitHub contributor graph
- Release notes
- PatchPanel membership
- Project acknowledgments

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CrowdCode! Together, we're building a more democratic, transparent, and collaborative approach to software development. 🚀
