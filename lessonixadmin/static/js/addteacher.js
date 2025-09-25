let subjects = [];
let rooms = [];

function addSubject() {
    const input = document.getElementById("subjectInput");
    const val = input.value.trim();

    if (val && !subjects.includes(val)) {
        subjects.push(val);
        renderTags("subjectList", subjects, "subject");
        updateHiddenFields();
    }
    input.value = "";
}

function addRoom() {
    const input = document.getElementById("roomInput");
    const val = input.value.trim();

    if (val && !rooms.includes(val)) {
        rooms.push(val);
        renderTags("roomList", rooms, "room");
        updateHiddenFields();
    }
    input.value = "";
}

function renderTags(containerId, arr, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";
    arr.forEach(item => {
        const tag = document.createElement("div");
        tag.className = "tag";
        tag.textContent = item;

        tag.onclick = () => removeTag(item, type);

        container.appendChild(tag);
    });
}

function removeTag(value, type) {
    if (type === "subject") {
        subjects = subjects.filter(s => s !== value);
        renderTags("subjectList", subjects, "subject");
    } else if (type === "room") {
        rooms = rooms.filter(r => r !== value);
        renderTags("roomList", rooms, "room");
    }
    updateHiddenFields();
}

// --- Оновлюємо приховані інпути ---
function updateHiddenFields() {
    document.getElementById("subjectsField").value = subjects.join(",");
    document.getElementById("roomsField").value = rooms.join(",");
}

// --- Валідація перед сабмітом ---
document.getElementById("addTeacherBtn").addEventListener("click", function (e) {
    if (subjects.length === 0 || rooms.length === 0) {
        e.preventDefault();
        alert("Будь ласка, додайте хоча б один предмет і одну кімнату!");
    }
});
