from flask import Flask, request, jsonify, abort, send_from_directory
from datetime import datetime, timezone
import itertools

app = Flask(__name__, static_folder="static", template_folder="templates")

tasks = {}
id_counter = itertools.count(1)

VALID_STATUS = {"pending", "in-progress", "completed"}
    
def utc_now():
    return datetime.now(timezone.utc).isoformat()

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data or not data["title"].strip():
        return jsonify({"error": "Title is required"}), 400

    task_id = next(id_counter)
    task = {
        "id": task_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "status": "pending",
        "created_at": utc_now()
    }
    tasks[task_id] = task
    return jsonify(task), 201

@app.route("/tasks", methods=["GET"])
def list_tasks():
    status_filter = request.args.get("status")
    result = list(tasks.values())

    if status_filter:
        if status_filter not in VALID_STATUS:
            return jsonify({"error": "Invalid status filter"}), 400
        result = [t for t in result if t["status"] == status_filter]

    return jsonify(result)

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task = tasks[task_id]

    if "title" in data:
        if not data["title"].strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        task["title"] = data["title"]

    if "description" in data:
        task["description"] = data["description"]

    if "status" in data:
        if data["status"] not in VALID_STATUS:
            return jsonify({"error": "Invalid status"}), 400
        task["status"] = data["status"]

    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    del tasks[task_id]
    return jsonify({"message": "Deleted"})
    
if __name__ == "__main__":
    app.run(debug=True)
