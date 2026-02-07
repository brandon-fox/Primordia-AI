# Contributing to Primordia-AI

This repository follows the organization-wide [Contributing Guidelines](https://github.com/vindicta-platform/.github/blob/main/CONTRIBUTING.md).

## 🔗 Pre-Commit Hooks (Required)

All developers **must** install and run pre-commit hooks before committing. This ensures:
- All markdown links are validated
- Code quality standards are enforced

### Setup

1. Install pre-commit:
   ```bash
   uv pip install pre-commit
   ```

2. Install hooks in your local repo:
   ```bash
   pre-commit install
   ```

3. Hooks run automatically on `git commit`. To run manually:
   ```bash
   pre-commit run --all-files
   ```
