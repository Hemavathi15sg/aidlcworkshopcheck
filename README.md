# Task Manager

A lightweight task management application with a **Python (Flask) REST API** and an **HTML/JavaScript frontend** served by the same Flask application. The folders remain separate for maintenance, but one process and one Azure App Service host both. Tasks are stored **in memory** and seeded from a JSON file at startup.

## Features

- Create, view, update and delete tasks (CRUD)
- Tasks displayed in an ID-sorted, paginated table with priority and area badges
- Previous/Next controls for navigating task pages
- In-app delete confirmation dialog
- Server-side validation of all task fields
- Interactive API documentation with Swagger UI
- Single PowerShell script to start the application

## Project Structure

```
Workshop/
├── run.ps1                  # Starts the application (frees port 5000 first)
├── .github/
│   └── workflows/
│       ├── ci-cd.yml        # Build, test, coverage, artifacts, deploy
│       └── codeql.yml       # Code scanning (Python + JavaScript)
├── app/
│   ├── backend/
│   │   ├── app.py               # Flask REST API
│   │   ├── openapi.py           # OpenAPI (Swagger) specification
│   │   ├── tasks.json           # Seed data loaded into memory at startup
│   │   ├── reports/             # Report files served by /api/reports
│   │   ├── tests/               # pytest test suite
│   │   ├── requirements.txt     # Runtime dependencies
│   │   └── requirements-dev.txt # Test dependencies
│   └── frontend/
│       ├── index.html           # UI layout and styles
│       └── app.js               # API integration and table rendering
```

## Task Fields

| Field        | Type    | Rules                                                                 |
|--------------|---------|-----------------------------------------------------------------------|
| `id`         | number  | Auto-generated                                                        |
| `title`      | string  | Required, max 200 characters                                          |
| `description`| string  | Optional, max 1000 characters                                         |
| `assignedTo` | string  | Mohan, Akshay, Praveen, Sandeep, Akash, Priya, Hema                   |
| `priority`   | number  | 1, 2, 3, 4 (1 = highest)                                              |
| `area`       | string  | Development, Testing, Deployment, Documentation, Design, Requirements |
| `startDate`  | date    | `YYYY-MM-DD`                                                          |
| `endDate`    | date    | `YYYY-MM-DD`, cannot be before `startDate`                            |

## Prerequisites

- Python 3.10+ (available on `PATH`)
- PowerShell 7+ (or Windows PowerShell 5.1)

## Getting Started

From the project root:

```powershell
.\run.ps1
```

The script will:
1. Stop any process using port **5000**
2. Install backend dependencies
3. Start Flask, serving both the API and frontend
4. Stop the app when you press **Ctrl+C**

If script execution is blocked, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

| App        | URL                              |
|------------|----------------------------------|
| Frontend   | http://localhost:5000            |
| API        | http://localhost:5000/api/tasks  |
| Swagger UI | http://localhost:5000/docs       |

### Run manually

```powershell
# One terminal - API and frontend
cd app/backend
pip install -r requirements.txt
python app.py
```

## API Endpoints

| Method | Endpoint               | Description                                  |
|--------|------------------------|----------------------------------------------|
| GET    | `/api/meta`            | Allowed values for assignees, areas, priority |
| GET    | `/api/tasks`           | List a page of tasks, sorted by ID ascending |
| GET    | `/api/tasks/{id}`      | Get a task by ID                             |
| GET    | `/api/tasks/search?q=` | Search tasks by title                        |
| GET    | `/api/reports?name=`   | Download a report file                       |
| POST   | `/api/tasks`           | Create a task                                |
| PUT    | `/api/tasks/{id}`      | Update a task                                |
| DELETE | `/api/tasks/{id}`      | Delete a task                                |

### List tasks

`GET /api/tasks` accepts these optional query parameters:

| Parameter  | Default | Limits       | Description           |
|------------|---------|--------------|-----------------------|
| `page`     | `1`     | 1 or greater | Page number            |
| `page_size`| `10`    | 1–50         | Tasks per page         |

The JSON response contains `items` (the tasks on this page), `page`, `page_size`,
`total` (all tasks), and `total_pages` (zero when there are no tasks). Tasks are
ordered by ascending ID. A page beyond the last page returns an empty `items` array.

Example request:

```text
GET http://localhost:5000/api/tasks?page=1&page_size=1
```

Example response:

```json
{
  "items": [
    {
      "id": 1,
      "title": "Conduct stakeholder workshops for the customer self-service portal",
      "description": "Run discovery sessions with Sales, Support and Finance to capture current pain points and must-have features. Get product owner sign-off on the requirements document.",
      "assignedTo": "Mohan",
      "priority": 1,
      "area": "Requirements",
      "startDate": "2026-09-21",
      "endDate": "2026-09-30"
    }
  ],
  "page": 1,
  "page_size": 1,
  "total": 15,
  "total_pages": 15
}
```

Invalid pagination returns status `400` with an `error` message: `page` and
`page_size` must be integers, `page` must be at least 1, and `page_size` must be
between 1 and 50.

In the frontend, **Previous** and **Next** navigate one page at a time. Previous is
disabled on the first page and Next on the last page; the indicator shows the
current page and total pages.

Example request:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/tasks -ContentType "application/json" -Body '{
  "title": "Prepare sprint demo",
  "description": "Create slides and demo script for the sprint review.",
  "assignedTo": "Priya",
  "priority": 2,
  "area": "Documentation",
  "startDate": "2026-10-10",
  "endDate": "2026-10-12"
}'
```

Errors are returned as `{"error": "message"}` with status `400` (validation) or `404` (not found).

## Configuration

| Setting           | Location                                   | Default                                         |
|-------------------|--------------------------------------------|-------------------------------------------------|
| API port          | `app/backend/app.py`                       | `5000`                                          |
| Frontend port     | Same Flask process as the API             | `5000`                                          |
| API base URL      | `app/frontend/app.js`                     | Same origin; relative `/api` requests            |
| Allowed origins   | `ALLOWED_ORIGINS` environment variable     | `http://localhost:8080,http://127.0.0.1:8080`   |

If you change the Flask port, update the launcher to match. The frontend uses the same origin automatically; CORS is not needed for this unified UI. The existing allowed-origins setting remains available for separate clients.

## Data Storage

- Tasks are loaded from `app/backend/tasks.json` into memory when the API starts.
- All create, update and delete operations change only the in-memory data.
- Restarting the API resets data back to the contents of `tasks.json`.

## Testing

```powershell
cd app/backend
pip install -r requirements.txt -r requirements-dev.txt
pytest -v --cov=app --cov=openapi --cov-report=term-missing
```

## CI/CD (GitHub Actions)

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `ci-cd.yml` | Push to `master` | Installs dependencies, compile check, runs tests with coverage, publishes test results and one `application` artifact |
| `dependency-review.yml` | PR to `master` | Fails the PR if it introduces a high-severity vulnerable dependency |
| `ci-cd.yml` → Deploy | Push to `master` (after tests pass) | Deploys the combined application to one Azure App Service |
| `codeql.yml` | Push / PR to `master` | CodeQL code scanning for Python and JavaScript |

### Azure setup for deployment

The step-by-step guide is in [Exercise 4: Deploy to Azure App Service](workshop/exercise-4-deploy-to-azure.md). Summary:

1. Create one **Linux, Python 3.12** App Service for the entire application. Add the app setting `SCM_DO_BUILD_DURING_DEPLOYMENT=true`, set the startup command below, and turn on **SCM Basic Auth Publishing Credentials**.
2. Download the web app's **publish profile** from its Overview page.
3. In GitHub **Settings → Secrets and variables → Actions → Secrets**, add the publish profile contents as the repository secret `AZURE_WEBAPP_PUBLISH_PROFILE`. Under **Variables**, add the repository variable `AZURE_APP_NAME`:

| Type | Name | Value |
|------|------|-------|
| Secret | `AZURE_WEBAPP_PUBLISH_PROFILE` | Full contents of the publish profile file |
| Repository variable | `AZURE_APP_NAME` | Single App Service name |

The deploy job is skipped until `AZURE_APP_NAME` is set.

The deployment package preserves `app/backend` and `app/frontend`, and copies the backend requirements into its root for Azure's build detection. Set the startup command in the App Service (**Settings → Configuration → Stack settings → Startup Command**): `gunicorn --chdir app/backend --bind=0.0.0.0:8000 --workers 1 --timeout 600 app:app`. Open the App Service URL for the frontend, `/api/tasks` for the API, and `/docs` for Swagger.

Keep one worker and one App Service instance while task data remains in memory. Restarts reset data, and multiple instances would maintain separate task lists; use persistent shared storage before scaling.

## Workshop Guide

Follow the hands-on guide starting at [Exercise 0: Introduction](workshop/exercise-0-introduction.md). It covers repository setup, pagination, a stacked README PR, Azure setup, and fixing a CI failure before deployment.

The exercises use `master`, the template's default branch, in commands and PR base branches.

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS, Flask-Swagger-UI
- **Frontend:** HTML, CSS, vanilla JavaScript (Fetch API)
