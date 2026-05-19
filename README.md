# GHAS Demo App — GH-500 Course

A deliberately vulnerable multi-language application for demonstrating **GitHub Advanced Security** features in the GH-500 course.

> **⚠️ WARNING:** This repository contains intentional security vulnerabilities and fake credentials for training purposes. **Do NOT deploy to production.**

## Repository Structure

```
GH500/
├── backend/                    # Python Flask app (vulnerable)
│   ├── app.py                  # Main app – SQL injection, hardcoded creds
│   ├── auth.py                 # Authentication – weak hashing, info leak
│   ├── requirements.txt        # Pinned to vulnerable versions
│   └── users.db                # (created at runtime)
├── frontend/                   # Node.js Express app (vulnerable)
│   ├── index.js                # XSS, path traversal
│   ├── package.json            # Pinned to vulnerable versions
│   └── .eslintrc.json          # ESLint config (for SARIF demo)
├── .github/
│   ├── dependabot.yml          # Dependabot version updates config
│   ├── secret_scanning.yml     # Secret scanning exclusions
│   ├── codeql/
│   │   └── codeql-config.yml   # Custom CodeQL configuration
│   └── workflows/
│       ├── codeql-analysis.yml       # CodeQL (advanced setup)
│       ├── dependency-review.yml     # Dependency review on PRs
│       └── eslint-sarif.yml          # Third-party SARIF upload
├── custom-queries/             # Custom CodeQL queries
│   ├── qlpack.yml
│   ├── hardcoded-credentials.ql
│   └── sql-injection-path.ql
├── credentials.yml             # INTENTIONAL leaked creds (fake)
├── config.env                  # INTENTIONAL leaked env vars (fake)
├── passwords.txt               # BFG replacement patterns (Demo 8.4)
├── SECURITY.md                 # Security policy
├── .gitignore
└── setup.ps1                   # One-click repo setup script
```

## Quick Setup

```powershell
# Clone
git clone https://github.com/SQLtattoo/GH500.git
cd GH500
```

## What Each Demo Uses

| Demo | Files Needed |
|------|-------------|
| 1.2 End-to-End PR | `backend/app.py`, `frontend/package.json`, `credentials.yml` |
| 2.1 Dependency Graph | `backend/requirements.txt`, `frontend/package.json` |
| 2.2 Enable Dependabot | `.github/dependabot.yml` |
| 2.3 Dependency Review | `.github/workflows/dependency-review.yml` |
| 2.5 GraphQL API | Any repo with Dependabot alerts |
| 3.2 Push Protection | `config.env` (push this to trigger block) |
| 3.3 Custom Patterns | `credentials.yml` (contains `INTERNAL_` tokens) |
| 4.1 Default Setup | Whole repo (language auto-detection) |
| 4.2 Advanced Setup | `.github/workflows/codeql-analysis.yml` |
| 4.3 Code Scanning PR | `backend/app.py` — create branch, introduce vuln |
| 4.5 Third-Party SARIF | `.github/workflows/eslint-sarif.yml`, `frontend/` |
| 5.1 CodeQL CLI | `backend/` (create database from this) |
| 5.3 Custom Query | `custom-queries/hardcoded-credentials.ql` |
| 5.4 Taint Tracking | `custom-queries/sql-injection-path.ql` |
| 6.2 Custom Config | `.github/codeql/codeql-config.yml` |
| 6.3 Language Matrix | `.github/workflows/codeql-analysis.yml` |
| 8.1 SECURITY.md | `SECURITY.md` |
| 8.4 Remove Data | `credentials.yml`, `config.env` |

## Intentional Vulnerabilities

### Python Backend (`backend/`)
- **SQL Injection** — `app.py:get_user()`, `app.py:search()` use f-string in SQL
- **Hardcoded Credentials** — `app.py` has DB password in source, `auth.py` has API keys
- **Weak Hashing** — `auth.py` uses MD5 for passwords
- **Information Disclosure** — `auth.py` leaks stack traces to users

### Node.js Frontend (`frontend/`)
- **XSS** — `index.js` reflects user input without sanitisation
- **Path Traversal** — `index.js` serves files from user-controlled path
- **Vulnerable Dependencies** — `package.json` pins old `lodash`, `express`, `follow-redirects`

### Leaked Secrets
- `credentials.yml` — Fake AWS keys, GitHub PAT, internal tokens
- `config.env` — Fake database URLs, API keys

## Prerequisites

- GitHub Org with **GHAS license** (or public repo for free features)
- Git, Node.js 18+, Python 3.10+
- CodeQL CLI (for Module 5 demos)
- VS Code + CodeQL extension (for Module 5 demos)
- BFG Repo-Cleaner + Java (for Demo 8.4)
