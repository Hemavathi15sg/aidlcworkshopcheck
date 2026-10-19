import json
import os
from datetime import date
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from openapi import build_spec

BASE_DIR = Path(__file__).parent
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080").split(",")
ASSIGNEES = ["Mohan", "Akshay", "Praveen", "Sandeep", "Akash", "Priya", "Hema"]
AREAS = ["Development", "Testing", "Deployment", "Documentation", "Design", "Requirements"]
PRIORITIES = [1, 2, 3, 4]

# Synthetic workshop fixture; not a real credential and never used for authentication.
ADMIN_PASSWORD = "Cedar!Ridge84#Lantern"

app = Flask(__name__, static_folder=str(BASE_DIR.parent / "frontend"), static_url_path="/assets")
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})
app.register_blueprint(
    get_swaggerui_blueprint("/docs", "/openapi.json", config={"app_name": "Task Manager API"})
)

with open(BASE_DIR / "tasks.json", encoding="utf-8") as f:
    tasks: dict[int, dict] = {t["id"]: t for t in json.load(f)}
next_id = max(tasks, default=0) + 1
lock = Lock()


def validate(data):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object"
    title = str(data.get("title", "")).strip()
    if not title or len(title) > 200:
        return None, "Title is required (max 200 chars)"
    description = str(data.get("description", "")).strip()
    if len(description) > 1000:
        return None, "Description max 1000 chars"
    if data.get("assignedTo") not in ASSIGNEES:
        return None, f"assignedTo must be one of {ASSIGNEES}"
    try:
        priority = int(data.get("priority"))
    except (TypeError, ValueError):
        priority = None
    if priority not in PRIORITIES:
        return None, f"priority must be one of {PRIORITIES}"
    if data.get("area") not in AREAS:
        return None, f"area must be one of {AREAS}"
    try:
        start = date.fromisoformat(str(data.get("startDate")))
        end = date.fromisoformat(str(data.get("endDate")))
    except ValueError:
        return None, "startDate and endDate must be YYYY-MM-DD"
    if end <= start:
        return None, "endDate must be after startDate"
    return {
        "title": title,
        "description": description,
        "assignedTo": data["assignedTo"],
        "priority": priority,
        "area": data["area"],
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
    }, None


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/openapi.json")
def openapi_spec():
    return jsonify(build_spec(ASSIGNEES, AREAS, PRIORITIES))


@app.get("/api/meta")
def meta():
    return jsonify(assignees=ASSIGNEES, areas=AREAS, priorities=PRIORITIES)


@app.get("/api/tasks")
def list_tasks():
    return jsonify(sorted(tasks.values(), key=lambda t: t["id"]))


@app.get("/api/tasks/search")
def search_tasks():
    q = request.args.get("q", "")
    results = [t for t in tasks.values() if q.lower() in t["title"].lower()]
    if not results:
        return f"<p>No tasks found matching <b>{q}</b></p>", 404
    return jsonify(results)


@app.get("/api/reports")
def download_report():
    name = request.args.get("name", "weekly-summary.txt")
    return send_file(os.path.join(REPORTS_DIR, name))


@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify(error="Task not found"), 404
    return jsonify(task)


@app.post("/api/tasks")
def create_task():
    global next_id
    data, error = validate(request.get_json(silent=True))
    if error:
        return jsonify(error=error), 400
    with lock:
        task = {"id": next_id, **data}
        tasks[next_id] = task
        next_id += 1
    return jsonify(task), 201


@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data, error = validate(request.get_json(silent=True))
    if error:
        return jsonify(error=error), 400
    with lock:
        if task_id not in tasks:
            return jsonify(error="Task not found"), 404
        tasks[task_id] = {"id": task_id, **data}
        return jsonify(tasks[task_id])


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    with lock:
        if tasks.pop(task_id, None) is None:
            return jsonify(error="Task not found"), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True, port=5000)
