# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 3.x     | :white_check_mark: |
| 2.x     | :white_check_mark: |
| 1.x     | :x:                |

## Reporting a Vulnerability

**Please do NOT open a public issue for security vulnerabilities.**

Instead, please report them via one of the following methods:

1. **GitHub Security Advisories:** Navigate to the Security tab of this
   repository and click "Report a vulnerability"
2. **Email:** security@example.com (PGP key available on request)

### What to Include
- Description of the vulnerability
- Steps to reproduce
- Impact assessment
- Suggested fix (if any)

### Response Timeline
- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 5 business days
- **Resolution Target:** Within 30 days for critical issues

## Security Technologies
- All dependencies are monitored by Dependabot
- Code scanning with CodeQL is enabled on all branches
- Secret scanning with push protection is active
- All commits to main require signed commits

## Compliance
This project follows OWASP Top 10 security guidelines.
