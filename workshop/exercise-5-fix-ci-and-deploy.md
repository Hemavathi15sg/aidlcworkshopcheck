# Exercise 5: Diagnose CI and Complete Deployment

**Goal:** Use Copilot to understand a failing Actions run, fix the issue in a PR, and verify deployment.

**Time:** 10-15 minutes

**Prerequisites:** The Exercise 3 stack is merged. Complete Exercise 4 first if you also want to deploy to Azure.

## Part A: Ask Copilot to explain the failure

1. Open the failed `CI/CD` run for the merge to `master` in **Actions**.
2. On the failed workflow run page, select **Explain error** to ask Copilot to analyze the workflow failure.
3. Copy Copilot's explanation and summarize the root cause. The expected failure is `test_create_same_day_task_is_allowed`: the test expects same-day tasks to be accepted, but validation currently rejects them.

## Part B: Fix the issue with Copilot

Create a fix branch from the latest `master`:

```powershell
git switch master
git pull --ff-only
git switch -c fix/same-day-task-validation
```

In Copilot Chat, provide the explanation from **Explain error** and ask:

> Use this CI failure summary to inspect the failing test and application code: [paste summary]. Make the smallest correct fix so tasks with the same start and end date are accepted, while tasks whose end date is before the start date remain invalid. Keep or add focused regression tests and avoid unrelated changes.

Review and accept the changes. Run the tests locally:

```powershell
Push-Location app\backend
pytest -v
Pop-Location
```

Confirm the same-day test passes and the earlier-end-date test still returns HTTP 400.

## Part C: Open a PR and redeploy

```powershell
git add app
git commit -m "Allow same-day tasks"
git push -u origin fix/same-day-task-validation
```

Open a PR into `master`. Review Copilot's suggestions if enabled, check CodeQL and Dependency Review, and get the required human approval. CI does not run on PRs; **Build & Test** runs when the fix is merged to `master`.

After merging, open **Actions** and confirm **Build & Test** passes. If Azure is configured in Exercise 4, confirm **Deploy to Azure App Service** succeeds and verify `/`, `/api/tasks`, and `/docs` on the App Service's default domain.

## Completion check

- [ ] Copilot's explanation identified the test failure and informed the fix.
- [ ] The fix PR was approved and merged; the same-day and earlier-end-date tests pass.
- [ ] **Build & Test** passed on `master`.
- [ ] If Azure was configured, deployment succeeded and the UI, API, and Swagger UI work.
