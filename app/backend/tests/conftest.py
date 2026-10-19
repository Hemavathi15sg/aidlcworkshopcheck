import importlib

import pytest

import app as app_module


@pytest.fixture
def client():
    # Reload so every test starts from the seed data in tasks.json
    module = importlib.reload(app_module)
    module.app.config["TESTING"] = True
    return module.app.test_client()


@pytest.fixture
def valid_task():
    return {
        "title": "Prepare sprint demo",
        "description": "Create slides and demo script for the sprint review.",
        "assignedTo": "Priya",
        "priority": 2,
        "area": "Documentation",
        "startDate": "2026-10-10",
        "endDate": "2026-10-12",
    }
