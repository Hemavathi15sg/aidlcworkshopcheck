# Exercise 1: Repository Setup and GitHub Advanced Security

**Goal:** Create your repository from the template, clone it, and enable Advanced Security features.

**Time:** 10-15 minutes

## Part A: Create your repository from the template

Follow [Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template) using the `CanarysPlayground/github-aidlc` template. 

- Set visibility to **Public** (Advanced Security is free for public repositories). 
- Do not add a README, `.gitignore`, or license.

## Part B: Clone and run

Clone **your** repository (not the template). The default branch is `master`.

```powershell
git clone https://github.com/YOUR-OWNER/YOUR-REPOSITORY.git
Set-Location YOUR-REPOSITORY
.\run.ps1
```

Open `http://localhost:5000` (app), `/api/tasks` (API), and `/docs` (Swagger UI). Stop with Ctrl+C. Never commit real credentials.

## Part C: Enable Advanced Security

Follow [Enabling security features at public repositories](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository#enabling-or-disabling-security-and-analysis-features-for-public-repositories) and enable:

- Dependabot alerts and security updates
- Code scanning
- Secret Protection: **Generic patterns**, **AI-detected secrets**, and **Push protection** (optionally a **Custom pattern**)

If a setting is unavailable, ask the facilitator.

## Part D: Verify CodeQL and CI-CD

The repository already includes `.github/workflows/codeql.yml` and `ci-cd.yml`, so CodeQL runs as **Advanced setup**. Do not configure CodeQL Default setup.

Open the **Actions** tab, enable workflows if a banner asks, and confirm `CodeQL` and `CI/CD` are listed.

## Part E: Protect `master`

Follow [Creating a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule#creating-a-branch-protection-rule) with:

- Target: **Include default branch** (or **Include by pattern** with `master`).
- Require a pull request with `1` approval.
- Block force pushes and deletions.
- Require secret scanning alerts to be resolved, and automatically request Copilot code review, if available.
- After all, keep the Enforcement status to **Active**, and click on **Create rule**.

## Completion check

- [ ] Public repository created from the template, cloned, and running on port 5000.
- [ ] Advanced Security features enabled; `CodeQL` and `CI/CD` workflows listed in Actions.
- [ ] `master` requires a PR with one approval and blocks force pushes and deletions.

Continue to [Exercise 2](exercise-2-feature-and-security-review.md).
