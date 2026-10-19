def test_frontend_is_served_by_api(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert b'/assets/app.js' in response.data
    assert b'http://localhost:5000' not in response.data
    asset = client.get("/assets/app.js")
    assert asset.status_code == 200
    assert b'const API_BASE = window.API_BASE_URL || "";' in asset.data
    assert client.get("/api/tasks").status_code == 200


def test_static_files_do_not_expose_backend(client):
    assert client.get("/assets/../backend/app.py").status_code == 404
    assert client.get("/assets/tasks.json").status_code == 404
    assert client.get("/api/not-found").status_code == 404


def test_list_tasks_returns_seed_data(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200
    ids = [t["id"] for t in res.json]
    assert len(ids) == 15
    assert ids == sorted(ids)


def test_get_task_by_id(client):
    res = client.get("/api/tasks/1")
    assert res.status_code == 200
    assert res.json["assignedTo"] == "Mohan"


def test_get_missing_task_returns_404(client):
    assert client.get("/api/tasks/999").status_code == 404


def test_meta_returns_dropdown_values(client):
    res = client.get("/api/meta")
    assert res.status_code == 200
    assert "Hema" in res.json["assignees"]
    assert "Deployment" in res.json["areas"]
    assert res.json["priorities"] == [1, 2, 3, 4]


def test_create_task(client, valid_task):
    res = client.post("/api/tasks", json=valid_task)
    assert res.status_code == 201
    assert res.json["id"] == 16
    assert client.get("/api/tasks/16").json["title"] == valid_task["title"]


def test_create_task_without_title_returns_400(client, valid_task):
    valid_task["title"] = "   "
    assert client.post("/api/tasks", json=valid_task).status_code == 400


def test_create_task_with_invalid_priority_returns_400(client, valid_task):
    valid_task["priority"] = 5
    assert client.post("/api/tasks", json=valid_task).status_code == 400


def test_create_task_with_unknown_assignee_returns_400(client, valid_task):
    valid_task["assignedTo"] = "John"
    assert client.post("/api/tasks", json=valid_task).status_code == 400


def test_create_task_with_end_before_start_returns_400(client, valid_task):
    valid_task["endDate"] = "2026-10-01"
    assert client.post("/api/tasks", json=valid_task).status_code == 400


def test_create_same_day_task_is_allowed(client, valid_task):
    valid_task["endDate"] = valid_task["startDate"]
    res = client.post("/api/tasks", json=valid_task)
    assert res.status_code == 201, res.json


def test_update_task(client, valid_task):
    res = client.put("/api/tasks/3", json=valid_task)
    assert res.status_code == 200
    assert res.json["id"] == 3
    assert client.get("/api/tasks/3").json["title"] == valid_task["title"]


def test_update_missing_task_returns_404(client, valid_task):
    res = client.put("/api/tasks/999", json=valid_task)
    assert res.status_code == 404


def test_delete_task(client):
    assert client.delete("/api/tasks/2").status_code == 204
    assert client.get("/api/tasks/2").status_code == 404


def test_delete_missing_task_returns_404(client):
    assert client.delete("/api/tasks/999").status_code == 404


def test_openapi_spec_is_served(client):
    res = client.get("/openapi.json")
    assert res.status_code == 200
    assert "/api/tasks" in res.json["paths"]
