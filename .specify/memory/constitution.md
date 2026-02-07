# Vindicta Platform Constitution

## Core Principles

### I. MCP-First Mandate
Always check for available MCP servers (GitHub, CloudRun, Firebase) before using CLI tools or manual scripts. For all GitHub, GCP, or Firebase operations, utilize the corresponding MCP tools. Manual CLI usage is a fallback only when MCP capabilities are exhausted.

### II. Spec-Driven Development (SDD)
Every feature implementation MUST start with an SDD bundle in `.specify/specs/[ID]-[name]/`. This bundle must include `spec.md`, `plan.md`, and `tasks.md`. Implementation cannot proceed until the SDD bundle is approved and merged into the main branch.

### III. Economic Prime Directive
All platform architecture and implementation must strictly comply with the GCP Free Tier. Scaling beyond free tier limits requires an explicit architectural review and justification.

### IV. Zero-Issue Stability
System stability and technical debt resolution take precedence over new feature development. When the "Repo-Guard" audit reveals high issue density or critical debt, the org shifts into a stabilization phase to maintain a "Zero-Issue State."

### V. Vanilla-Forward & Modern Tooling
Favor vanilla JavaScript (ES2020+) and modern build systems (Vite 7+) over heavy frameworks. Maintain compatibility with Firebase SDK v10+ and leverage GitHub Actions for all CI/CD pipelines.

## Quality Gates

1. **Linting & Formatting**: All commits must pass pre-commit hooks and linting checks.
2. **Test Coverage**: Critical paths must have associated unit or integration tests.
3. **Link Integrity**: Documentation must pass markdown link validation.
4. **Agent Context**: Every repository must contain up-to-date `.antigravity/` context artifacts (`ARCHITECTURE.md`, `CONSTRAINTS.md`).

## Governance
This constitution supersedes all individual repository practices. Amendments require approval from the Platform Lead and must be documented in this file.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
