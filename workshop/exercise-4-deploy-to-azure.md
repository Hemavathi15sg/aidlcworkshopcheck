# Exercise 4 (Optional): Deploy to Azure App Service

**Goal:** Prepare Azure App Service and GitHub settings for deployment.

**Time:** 15-20 minutes

Prerequisites: Have Azure access listed in [Exercise 0](exercise-0-introduction.md#prerequisites). If deploying, complete this setup before merging the Exercise 3 stack. The deployment workflow runs on a push or merge to `master` after **Build & Test** succeeds.

## Part A: Create the web app

Follow Microsoft's [Python App Service quickstart](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli#create-a-web-app-in-azure) to create a web app in the Azure portal. Use these settings:

| Setting | Value |
|---------|-------|
| Name | Unique name; use this as `AZURE_APP_NAME` |
| Publish | Code |
| Runtime stack | Python 3.12 |
| Operating System | Linux |
| Region | Nearest region |
| Pricing plan | Free F1 (recommended) |


## Part B: Configure App Service

After creating the web app, in app settings:

1. Open **Settings → Configuration → General settings**, enable **SCM Basic Auth Publishing Credentials**, and save. This is required to use the publish profile.

2. Under **Environment variables → App settings**, add `SCM_DO_BUILD_DURING_DEPLOYMENT=true` and save.
3. Under **Configuration → Stack settings**, set the startup command:

   ```text
   gunicorn --chdir app/backend --bind=0.0.0.0:8000 --workers 1 --timeout 600 app:app
   ```

## Part C: Add GitHub settings

For steps, see GitHub's guide to [creating repository secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets#creating-secrets-for-a-repository).

1. From the App Service **Overview**, download the publish profile. Treat it as a password.
2. In **Settings → Secrets and variables → Actions**, create a repository secret named `AZURE_WEBAPP_PUBLISH_PROFILE` and paste the complete, unedited profile contents.
3. On the **Variables** tab, create a repository variable named `AZURE_APP_NAME` with the exact App Service name.
4. Delete the downloaded profile. Never commit or share it. If exposed, reset it and update the secret.

## Completion check

- [ ] Linux App Service created with Python 3.12, publishing credentials enabled, the build setting, and startup command.
- [ ] `AZURE_WEBAPP_PUBLISH_PROFILE` repository secret and `AZURE_APP_NAME` repository variable are configured.
