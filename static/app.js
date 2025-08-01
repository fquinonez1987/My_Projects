// Codigo de la logica (app.js)

// Aquí controlamos:

// Registro/Login (pide token).

// Guardamos token en localStorage.

// Usamos token para todas las peticiones (Authorization: Bearer <token>).

// Mostrar/ocultar secciones según si el usuario está logueado.

const API_URL = 'http://127.0.0.1:5000';
let token = localStorage.getItem('token');

function showSection() {
    document.getElementById("auth").style.display = token ? "none" : "block";
    document.getElementById("todo").style.display = token ? "block" : "none";
    if (token) fetchTasks();
}

async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content=Type": "application/json"},
        body: JSON.stringify({username, password})
    });
    const data = await res.json();
    document.getElementById("authMsg").innerText = data.message || data.error;
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const res = await fetch (`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });
    const data = await res.json();
    if (data.token){
        token = data.token;
        localStorage.setItem("token", token);
        showSection();
    } else {
        document.getElementById("authMsg").innerText = data.error || "Login fallido";
    }
}

function logout() {
    token = null;
    localStorage.removeItem("token");
    showSection();
}

async function fetchTasks() {
    const res = await fetch (`${API_URL}/tasks`, {
        header: {"Authorization": `Bearer ${token}`}
    });
    const tasks = await res.json();
    const list = await res.json();
    list.innerHTML = "";
    tasks.forEach(task => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${task.completed ? `<s>${task.title}</s>` : task.title}
            <div>
                <button onclick="toggleTask(${task.id}, ${!task.completed})">${task.completed ? "Desmarcar": "Completar"}</button>
                <button onclick ="deleteTask(${task.id})"> Eliminar </button>
            </div>
        `;
        list.appendChild(li);
    });
}

async function addTask() {
    const input = document.getElementById("taskInput");
    if (!input.value)return;
    await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify({title: input.value})
    });
    input.value = "";
    fetchTasks();
}

async function toggleTask(id, completed) {
    await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
        body: JSON.stringify({completed})
    });
    fetchTasks();
}

async function deleteTask(id) {
    await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
        headers: {"Authorization": `Bearer ${token}`}
    });
    fetchTasks();
}

showSection();
