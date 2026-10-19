import pytest


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
    assert res.json["page"] == 1
    assert res.json["page_size"] == 10
    assert res.json["total"] == 15
    assert res.json["total_pages"] == 2
    ids = [t["id"] for t in res.json["items"]]
    assert len(ids) == 10
    assert ids == sorted(ids)


def test_list_tasks_returns_requested_page(client):
    res = client.get("/api/tasks?page=2&page_size=5")
    assert res.status_code == 200
    all_tasks = client.get("/api/tasks?page_size=50").json["items"]
    assert res.json["items"] == all_tasks[5:10]
    assert res.json["page"] == 2
    assert res.json["page_size"] == 5
    assert res.json["total"] == 15
    assert res.json["total_pages"] == 3


def test_list_tasks_accepts_maximum_page_size(client):
    res = client.get("/api/tasks?page_size=50")
    assert res.status_code == 200
    assert res.json["page_size"] == 50
    assert len(res.json["items"]) == 15
    assert res.json["total_pages"] == 1


@pytest.mark.parametrize(
    ("query", "error"),
    [
        ("page=abc", "page must be an integer"),
        ("page_size=abc", "page_size must be an integer"),
        ("page=0", "page must be at least 1"),
        ("page_size=0", "page_size must be between 1 and 50"),
        ("page_size=51", "page_size must be between 1 and 50"),
    ],
)
def test_list_tasks_rejects_invalid_pagination(client, query, error):
    res = client.get(f"/api/tasks?{query}")
    assert res.status_code == 400
    assert res.json == {"error": error}


def test_list_tasks_returns_empty_pagination_metadata(client):
    from app import tasks

    tasks.clear()
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert res.json == {
        "items": [],
        "page": 1,
        "page_size": 10,
        "total": 0,
        "total_pages": 0,
    }


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
    list_tasks = res.json["paths"]["/api/tasks"]["get"]
    assert [param["name"] for param in list_tasks["parameters"]] == ["page", "page_size"]
    assert list_tasks["responses"]["400"]
    assert (
        list_tasks["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/PaginatedTasks"
    )
