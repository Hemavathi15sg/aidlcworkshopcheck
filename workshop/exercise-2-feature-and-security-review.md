# Exercise 2: Server-Side Pagination, Pull Request, and GitHub Advanced Security Review

**Goal:** Add server-side pagination, open a pull request, and review CodeQL and secret scanning results.

**Time:** 5-10 minutes

## Part A: Check the current app

```powershell
.\run.ps1
```

Open `http://localhost:5000` and note that all 15 tasks load in one list, with no pagination. Stop with Ctrl+C.

## Part B: Create and switch to a feature branch

Start from the latest `master`, then create and switch to a new feature branch:

```powershell
git switch master
git pull --ff-only
git switch -c feature/server-pagination
git branch --show-current
```

Confirm the output is `feature/server-pagination`. Keep this branch active while implementing the feature.

## Part C: Implement server-side pagination

In Copilot Chat, use these files from Explorer into the chat to provide context:

- [app.py](../app/backend/app.py) - backend API.
- [app.js](../app/frontend/app.js) - frontend logic.
- [index.html](../app/frontend/index.html) - table and controls.
- [openapi.py](../app/backend/openapi.py) - API definition.

Then use this prompt:

> Add server-side pagination to `GET /api/tasks`, sorted by ID ascending: `page` defaults to 1; `page_size` defaults to 10 (max 50). Return `{items, page, page_size, total, total_pages}`, with `total_pages: 0` for no tasks. Return HTTP 400 JSON errors for non-integers, `page < 1`, or `page_size` outside 1–50. Fetch only the active page in the frontend; add accessible Previous/Next buttons disabled at boundaries and a page indicator. Update OpenAPI and backend tests, preserving existing features.
>
> Edit only the source code files under `app/`.

After Copilot finishes, review and accept the code changes. Check `git diff --stat` to confirm that only the intended code, OpenAPI, and test files under `app/` changed. Then run the app and check the pagination feature:

```powershell
.\run.ps1
```

Open `http://localhost:5000` and confirm Previous/Next, the page indicator, and the disabled buttons at the first and last page work. Stop with Ctrl+C.

## Part D: Push and open a pull request

```powershell
git add app
git commit -m "Add server-side task pagination"
git push -u origin feature/server-pagination
```

Select **Compare & pull request** and create a non-draft PR targeting `master` with a brief summary.

- **Copilot review:** wait for automatic review, read comments under **Files changed**, and commit relevant fixes to `feature/server-pagination`. If review does not start, check the automatic review ruleset.
- **Checks:** review **CodeQL** and **Dependency Review** results. These run when the PR opens; **Build & Test** runs on pushes to `master`, including merges.

**Leave the PR open for Exercise 3**, which stacks a documentation PR on this branch. One human approval is required; Copilot review does not count.

## Part E: Review security alerts and generate a fix with Copilot

> **Note:** Wait for CodeQL and Dependency Review to finish. Secret scanning runs separately.

### Review the alerts

Open **Security and quality** and review alerts, including existing findings on `master`:

- **Dependabot > Vulnerabilities:** affected packages and available security updates.
- **Code scanning:** affected code, severity, and recommended fixes.
- **Secret scanning:** exposed secrets. The synthetic password may not be detected; never use real credentials.

Record findings or note that no alerts appeared.

### Use Copilot Autofix on a code scanning alert

1. Open a supported alert, select **Generate fix**, and review the suggestion.
2. Select **Commit to branch** (existing branch) or **Commit to new branch**, then confirm. No new PR is required.
3. Fetch the branch locally, pull if it is your current branch, and test the fix.
4. Create a PR if you have committed the changes to a new branch.

Reference: [Resolving code scanning alerts with Copilot Autofix](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/resolve-alerts#generating-a-suggested-fix).

## Completion check

- [ ] Pagination is done by the API, tested, and works at `http://localhost:5000`.
- [ ] Pull request into `master` is open and its checks passed.
- [ ] Dependabot, code scanning, and secret scanning alerts were reviewed and findings recorded; no real secrets were committed.
- [ ] A Copilot Autofix suggestion was reviewed, committed to an existing or new branch, and tested, or its unavailability was recorded.

Continue to [Exercise 3](exercise-3-readme-update.md).
