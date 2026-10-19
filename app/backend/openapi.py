def build_spec(assignees, areas, priorities):
    task_input = {
        "type": "object",
        "required": ["title", "assignedTo", "priority", "area", "startDate", "endDate"],
        "properties": {
            "title": {"type": "string", "maxLength": 200, "example": "Build REST endpoints for order history"},
            "description": {"type": "string", "maxLength": 1000, "example": "Develop order endpoints with filters and sorting."},
            "assignedTo": {"type": "string", "enum": assignees, "example": assignees[0]},
            "priority": {"type": "integer", "enum": priorities, "example": 1},
            "area": {"type": "string", "enum": areas, "example": areas[0]},
            "startDate": {"type": "string", "format": "date", "example": "2026-10-08"},
            "endDate": {"type": "string", "format": "date", "example": "2026-10-17"},
        },
    }
    task = {
        "allOf": [
            {"type": "object", "properties": {"id": {"type": "integer", "example": 1}}},
            {"$ref": "#/components/schemas/TaskInput"},
        ]
    }
    error = {"type": "object", "properties": {"error": {"type": "string"}}}
    task_id_param = {"name": "task_id", "in": "path", "required": True, "schema": {"type": "integer"}}

    def json_response(description, schema_ref):
        return {"description": description, "content": {"application/json": {"schema": {"$ref": schema_ref}}}}

    not_found = json_response("Task not found", "#/components/schemas/Error")
    bad_request = json_response("Validation error", "#/components/schemas/Error")
    task_body = {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TaskInput"}}}}

    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Task Manager API",
            "version": "1.0.0",
            "description": "In-memory task API. Data is seeded from tasks.json and reset on restart.",
        },
        "servers": [{"url": "/"}],
        "tags": [{"name": "Tasks"}, {"name": "Reports"}, {"name": "Metadata"}],
        "paths": {
            "/api/meta": {
                "get": {
                    "tags": ["Metadata"],
                    "summary": "Get allowed values for dropdowns",
                    "responses": {"200": json_response("Allowed values", "#/components/schemas/Meta")},
                }
            },
            "/api/tasks": {
                "get": {
                    "tags": ["Tasks"],
                    "summary": "List all tasks",
                    "responses": {
                        "200": {
                            "description": "List of tasks",
                            "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Task"}}}},
                        }
                    },
                },
                "post": {
                    "tags": ["Tasks"],
                    "summary": "Create a task",
                    "requestBody": task_body,
                    "responses": {"201": json_response("Task created", "#/components/schemas/Task"), "400": bad_request},
                },
            },
            "/api/tasks/search": {
                "get": {
                    "tags": ["Tasks"],
                    "summary": "Search tasks by title",
                    "parameters": [{"name": "q", "in": "query", "schema": {"type": "string"}, "example": "invoice"}],
                    "responses": {
                        "200": {
                            "description": "Matching tasks",
                            "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Task"}}}},
                        },
                        "404": {"description": "No matching tasks", "content": {"text/html": {"schema": {"type": "string"}}}},
                    },
                }
            },
            "/api/reports": {
                "get": {
                    "tags": ["Reports"],
                    "summary": "Download a report file",
                    "parameters": [{"name": "name", "in": "query", "schema": {"type": "string"}, "example": "weekly-summary.txt"}],
                    "responses": {"200": {"description": "Report file", "content": {"text/plain": {"schema": {"type": "string"}}}}},
                }
            },
            "/api/tasks/{task_id}": {
                "parameters": [task_id_param],
                "get": {
                    "tags": ["Tasks"],
                    "summary": "Get a task by ID",
                    "responses": {"200": json_response("Task", "#/components/schemas/Task"), "404": not_found},
                },
                "put": {
                    "tags": ["Tasks"],
                    "summary": "Update a task",
                    "requestBody": task_body,
                    "responses": {
                        "200": json_response("Task updated", "#/components/schemas/Task"),
                        "400": bad_request,
                        "404": not_found,
                    },
                },
                "delete": {
                    "tags": ["Tasks"],
                    "summary": "Delete a task",
                    "responses": {"204": {"description": "Task deleted"}, "404": not_found},
                },
            },
        },
        "components": {
            "schemas": {
                "TaskInput": task_input,
                "Task": task,
                "Error": error,
                "Meta": {
                    "type": "object",
                    "properties": {
                        "assignees": {"type": "array", "items": {"type": "string"}, "example": assignees},
                        "areas": {"type": "array", "items": {"type": "string"}, "example": areas},
                        "priorities": {"type": "array", "items": {"type": "integer"}, "example": priorities},
                    },
                },
            }
        },
    }
