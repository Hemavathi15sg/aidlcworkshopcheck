const API_BASE = window.API_BASE_URL || "";
const API = `${API_BASE}/api/tasks`;
const form = document.getElementById("taskForm");
const body = document.getElementById("taskBody");
const message = document.getElementById("message");
const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");
const fields = ["title", "description", "assignedTo", "priority", "area", "startDate", "endDate"];
const $ = (id) => document.getElementById(id);

function fillSelect(id, values) {
  const select = $(id);
  values.forEach((v) => select.add(new Option(v, v)));
}

async function request(url, options = {}) {
  const res = await fetch(url, { headers: { "Content-Type": "application/json" }, ...options });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `Request failed (${res.status})`);
  }
  return res.status === 204 ? null : res.json();
}

function cell(row, text) {
  const td = row.insertCell();
  td.textContent = text;
  return td;
}

function badgeCell(row, text, className) {
  const span = document.createElement("span");
  span.className = `badge ${className}`;
  span.textContent = text;
  row.insertCell().append(span);
}

function actionButton(label, className, onClick) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = `sm ${className}`;
  btn.textContent = label;
  btn.onclick = onClick;
  return btn;
}

async function loadTasks() {
  const tasks = await request(API);
  body.replaceChildren();
  tasks.forEach((t) => {
    const row = body.insertRow();
    cell(row, t.id);
    cell(row, t.title);
    cell(row, t.description);
    cell(row, t.assignedTo);
    badgeCell(row, `P${t.priority}`, `p${t.priority}`);
    badgeCell(row, t.area, "area");
    cell(row, t.startDate);
    cell(row, t.endDate);
    const actions = document.createElement("div");
    actions.className = "row-actions";
    actions.append(
      actionButton("Edit", "link", () => startEdit(t)),
      actionButton("Delete", "link-danger", () => deleteTask(t))
    );
    row.insertCell().append(actions);
  });
}

function startEdit(task) {
  $("taskId").value = task.id;
  fields.forEach((f) => ($(f).value = task[f]));
  saveBtn.textContent = "Update Task";
  $("formTitle").textContent = `Edit Task #${task.id}`;
  cancelBtn.hidden = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetForm() {
  form.reset();
  $("taskId").value = "";
  saveBtn.textContent = "Add Task";
  $("formTitle").textContent = "Add Task";
  cancelBtn.hidden = true;
}

function confirmDialog(text) {
  const dialog = $("confirmDialog");
  $("confirmText").textContent = text;
  dialog.returnValue = "";
  dialog.showModal();
  return new Promise((resolve) =>
    dialog.addEventListener("close", () => resolve(dialog.returnValue === "ok"), { once: true })
  );
}

async function deleteTask(task) {
  if (!(await confirmDialog(`Are you sure you want to delete task #${task.id} "${task.title}"? This cannot be undone.`))) return;
  try {
    await request(`${API}/${task.id}`, { method: "DELETE" });
    message.textContent = "";
    await loadTasks();
  } catch (e) {
    message.textContent = e.message;
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(fields.map((f) => [f, $(f).value]));
  data.priority = Number(data.priority);
  const id = $("taskId").value;
  try {
    await request(id ? `${API}/${id}` : API, {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(data),
    });
    message.textContent = "";
    resetForm();
    await loadTasks();
  } catch (err) {
    message.textContent = err.message;
  }
});

cancelBtn.addEventListener("click", resetForm);

const user = new URLSearchParams(location.search).get("user");
if (user) $("welcome").innerHTML = `Welcome back, <strong>${user}</strong>`;

(async () => {
  try {
    const meta = await request(`${API_BASE}/api/meta`);
    fillSelect("assignedTo", meta.assignees);
    fillSelect("priority", meta.priorities);
    fillSelect("area", meta.areas);
    await loadTasks();
  } catch (e) {
    message.textContent = `Cannot reach API at ${API_BASE}: ${e.message}`;
  }
})();
