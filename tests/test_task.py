import pytest
from app import app, reset_state


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        reset_state()  
        yield client


def test_create_task(client):
    res = client.post("/tasks", json={"title": "Test"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["status"] == "pending"

def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task1"})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.get_json()) == 1

def test_missing_title(client):
    res = client.post("/tasks", json={"description": "No title"})
    assert res.status_code == 400

def test_update_status(client):
    res = client.post("/tasks", json={"title": "Task"})
    task_id = res.get_json()["id"]

    res = client.put(f"/tasks/{task_id}", json={"status": "completed"})
    assert res.status_code == 200
    assert res.get_json()["status"] == "completed"

def test_filter_status(client):
    client.post("/tasks", json={"title": "T1"})
    client.post("/tasks", json={"title": "T2"})
    client.put("/tasks/2", json={"status": "completed"})

    res = client.get("/tasks?status=completed")
    assert len(res.get_json()) == 1

def test_delete_task(client):
    client.post("/tasks", json={"title": "Task"})
    res = client.delete("/tasks/1")
    assert res.status_code == 200

def test_invalid_status(client):
    res = client.post("/tasks", json={"title": "Task"})
    task_id = res.get_json()["id"]

    res = client.put(f"/tasks/{task_id}", json={"status": "invalid"})
    assert res.status_code == 400

def test_nonexistent_id(client):
    res = client.put("/tasks/999", json={"status": "completed"})
    assert res.status_code == 404