<#
.SYNOPSIS
    One-click setup for the ghas-demo-app repository on GitHub.

.DESCRIPTION
    Creates a new GitHub repository, initialises it with all demo files,
    and pushes the initial commit. Requires the GitHub CLI (gh) to be
    installed and authenticated.

.PARAMETER OrgName
    The GitHub organisation (or username) to create the repo under.

.PARAMETER RepoName
    Repository name. Defaults to "ghas-demo-app".

.PARAMETER Visibility
    Repository visibility: public, private, or internal. Defaults to private.

.EXAMPLE
    .\setup.ps1 -OrgName "my-org"
    .\setup.ps1 -OrgName "my-org" -RepoName "ghas-demo" -Visibility public
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$OrgName,

    [string]$RepoName = "ghas-demo-app",

    [ValidateSet("public", "private", "internal")]
    [string]$Visibility = "private"
)

$ErrorActionPreference = "Stop"

# --- Pre-flight checks ---
Write-Host "`n=== GH-500 Demo Repo Setup ===" -ForegroundColor Cyan

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) is not installed. Install from https://cli.github.com"
}

$ghStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "GitHub CLI is not authenticated. Run 'gh auth login' first."
}

Write-Host "Creating repository $OrgName/$RepoName ($Visibility)..." -ForegroundColor Yellow

# --- Create the repo ---
gh repo create "$OrgName/$RepoName" `
    --$Visibility `
    --description "GH-500 Demo: Deliberately vulnerable app for GHAS training" `
    --confirm 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Repository may already exist. Continuing..." -ForegroundColor DarkYellow
}

# --- Initialise git and push ---
$repoRoot = Split-Path -Parent $PSScriptRoot
if ($repoRoot -eq "") { $repoRoot = $PSScriptRoot }

Push-Location $repoRoot

if (-not (Test-Path ".git")) {
    git init
    git branch -M main
}

# Set remote
$remoteUrl = "https://github.com/$OrgName/$RepoName.git"
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    git remote set-url origin $remoteUrl
} else {
    git remote add origin $remoteUrl
}

# Stage and commit everything
git add -A
git commit -m "Initial commit: GH-500 demo app with intentional vulnerabilities

This repo contains:
- Python Flask backend with SQL injection vulns
- Node.js Express frontend with XSS and path traversal
- Vulnerable dependency versions (Dependabot demos)
- Fake credentials (secret scanning demos)
- GitHub Actions workflows (CodeQL, dependency-review, ESLint SARIF)
- Custom CodeQL queries
- SECURITY.md policy

DO NOT deploy to production."

Write-Host "Pushing to $remoteUrl ..." -ForegroundColor Yellow
git push -u origin main

Pop-Location

# --- Post-setup instructions ---
Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host @"

Next steps (in the GitHub UI):
1. Go to Settings > Code security and analysis
2. Enable: Dependency graph, Dependabot alerts, Dependabot security updates
3. Enable: GitHub Advanced Security (if private repo)
4. Enable: Secret scanning + Push protection
5. Enable: Code scanning > Default setup  (or let the workflow handle it)

Repository URL: https://github.com/$OrgName/$RepoName

"@ -ForegroundColor White
