async function createTask() {
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!title) {
        alert("Title is required");
        return;
    }

    const res = await fetch("/tasks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ title, description })
    });

    if (!res.ok) {
        const err = await res.json();
        alert(err.error || "Error creating task");
        return;
    }

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    loadTasks();
}

async function loadTasks() {
    const filter = document.getElementById("filter").value;
    const url = filter ? `/tasks?status=${filter}` : "/tasks";

    const res = await fetch(url);
    const tasks = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    if (tasks.length === 0) {
        list.innerHTML = "<p>No tasks found</p>";
        return;
    }

tasks.forEach(task => {
    const li = document.createElement("li");

        li.innerHTML = `
        <div class="task-info">
            <input class="edit-title" value="${task.title}" disabled>
            <input class="edit-desc" value="${task.description}" disabled>

            <select class="edit-status" disabled>
                <option value="pending" ${task.status === "pending" ? "selected" : ""}>Pending</option>
                <option value="in-progress" ${task.status === "in-progress" ? "selected" : ""}>In Progress</option>
                <option value="completed" ${task.status === "completed" ? "selected" : ""}>Completed</option>
            </select>
        </div>

        <div class="task-actions">
            <div class="buttons">
                <button onclick="enableEdit(this)">Edit</button>
                <button onclick="saveEdit(${task.id}, this)" class="save-btn" hidden>Save</button>
                <button onclick="cancelEdit(this)" class="cancel-btn" hidden>Cancel</button>
                <button onclick="deleteTask(${task.id})">Delete</button>
            </div>

            <div class="task-meta">
                <span>ID: ${task.id}</span>
                <span>${new Date(task.created_at).toLocaleString()}</span>
            </div>
        </div>
    `;


    list.appendChild(li);
});

}

async function updateStatus(id, currentStatus) {
    const cycle = ["pending", "in-progress", "completed"];
    const next = cycle[(cycle.indexOf(currentStatus) + 1) % cycle.length];

    await fetch(`/tasks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ status: next })
    });

    loadTasks();
}

async function deleteTask(id) {
    await fetch(`/tasks/${id}`, { method: "DELETE" });
    loadTasks();
}

loadTasks();

function enableEdit(btn) {
    const li = btn.closest("li");

    li.querySelector(".edit-title").disabled = false;
    li.querySelector(".edit-desc").disabled = false;
    li.querySelector(".edit-status").disabled = false;

    li.querySelector(".save-btn").hidden = false;
    li.querySelector(".cancel-btn").hidden = false;

    btn.hidden = true;
}

function cancelEdit(btn) {
    loadTasks();  
}

async function saveEdit(id, btn) {
    const li = btn.closest("li");

    const title = li.querySelector(".edit-title").value.trim();
    const description = li.querySelector(".edit-desc").value.trim();
    const status = li.querySelector(".edit-status").value;

    if (!title) {
        alert("Title cannot be empty");
        return;
    }

    const res = await fetch(`/tasks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ title, description, status })
    });

    if (!res.ok) {
        const err = await res.json();
        alert(err.error || "Update failed");
        return;
    }

    loadTasks();
}
