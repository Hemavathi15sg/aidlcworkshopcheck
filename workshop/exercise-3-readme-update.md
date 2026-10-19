# Exercise 3: Stacked PR — Update the README with Copilot

**Goal:** Document pagination in `README.md`, open a stacked PR, and merge both PRs.

**Time:** 5-10 minutes

## Part A: Create a documentation branch

Keep the pagination PR open and branch from `feature/server-pagination`:

```powershell
git switch feature/server-pagination
git pull --ff-only
git switch -c docs/readme-pagination
```

## Part B: Document pagination

In Copilot Chat, use these files from Explorer into the chat to provide context:

- [README.md](../README.md) - documentation to update.
- [app.py](../app/backend/app.py) - backend API and validation.
- [app.js](../app/frontend/app.js) - pagination logic.
- [index.html](../app/frontend/index.html) - table and controls.
- [openapi.py](../app/backend/openapi.py) - API definition.

Then use this prompt:

> Update only `README.md` to document task pagination based on the current code. Cover `GET /api/tasks` parameters, defaults and limits, response fields, an example request and response, validation errors, and Previous/Next controls. Update existing descriptions for consistency. Keep it concise and preserve unrelated content.

Review and accept the changes. Check accuracy against the app and confirm `git diff --stat` lists only `README.md`.

## Part C: Commit and open a stacked pull request

```powershell
git add README.md
git commit -m "Document task pagination in README"
git push -u origin docs/readme-pagination
```

Create a PR from `docs/readme-pagination` into **`feature/server-pagination`**, not `master`. This stacks the documentation on the pagination PR. Select **Create stack** or accept the stack banner if offered. Confirm **Files changed** lists only `README.md`.

CodeQL and Dependency Review do not run while this PR targets the feature branch. CI runs on pushes to `master`.

## Part D: Approve and merge the stack

> **Note:** If you have Azure portal access and permission to create a web app, complete [Exercise 4: Deploy to Azure](exercise-4-deploy-to-azure.md) before merging, then return here. Otherwise, skip the optional Azure setup and continue below. After merging, continue to [Exercise 5](exercise-5-fix-ci-and-deploy.md) to diagnose the CI failure and, if configured, deploy.

1. Ask a facilitator or teammate with write access to approve each PR. Self-approval and Copilot review do not satisfy the required human approval.
2. Merge the pagination PR first. Confirm the README PR now targets `master` (change its base if needed), review its checks, then merge it.
3. Confirm CodeQL succeeds in **Actions**. `Build & Test` is expected to fail on the intentionally failing same-day task test, so deployment is skipped. Exercise 5 fixes it. Update local `master` and check the README:

```powershell
git switch master
git pull --ff-only
```

## Completion check

- [ ] Only `README.md` changed in the documentation PR, accurately describing pagination.
- [ ] Both PRs received human approval and merged bottom up; CodeQL succeeded and the expected CI failure is noted for Exercise 5.

Continue to [Exercise 5](exercise-5-fix-ci-and-deploy.md) after the merge to fix the CI failure and, if configured, deploy the app.
