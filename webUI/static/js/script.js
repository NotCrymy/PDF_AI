// ============================================================
// Documents
// ============================================================

const documentList = document.getElementById("document-list");

async function loadDocuments() {

    console.log("Loading documents...");

    try {

        const response = await fetch("/api/documents");

        console.log("Status:", response.status);

        if (!response.ok) {
            throw new Error(`Failed to load documents: ${response.status}`);
        }

        const documents = await response.json();

        console.log("Documents:", documents);

        documentList.innerHTML = "";

        for (const doc of documents) {
            addDocumentToList(doc);
        }

    } catch (error) {

        console.error("Error loading documents:", error);

    }
}


function addDocumentToList(doc) {

    const documentElement = document.createElement("div");

    documentElement.className = "document-item";

    documentElement.innerHTML = `
        <div class="document-icon">
            PDF
        </div>

        <div class="document-info">
            <div class="document-name">
                ${escapeHtml(doc.name)}
            </div>
        </div>

        <button
            class="document-delete"
            type="button"
            title="Delete document"
        >
            ×
        </button>
    `;

    const deleteButton = documentElement.querySelector(".document-delete");

    deleteButton.addEventListener("click", async (event) => {

        event.stopPropagation();

        const confirmed = confirm(
            `Delete "${doc.name}"?`
        );

        if (!confirmed) {
            return;
        }

        try {

            const response = await fetch(
                `/api/documents/${encodeURIComponent(doc.name)}`,
                {
                    method: "DELETE"
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Delete failed: ${response.status}`
                );
            }

            documentList.removeChild(documentElement);

        } catch (error) {

            console.error("Delete error:", error);

        }
    });

    documentList.appendChild(documentElement);
}


function escapeHtml(text) {

    const element = document.createElement("div");

    element.textContent = text;

    return element.innerHTML;
}

const deleteAllButton = document.getElementById("delete-all-documents");

deleteAllButton.addEventListener("click", async () => {

    const confirmed = confirm("Delete all documents?");

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch("/api/documents", {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error(`Delete failed: ${response.status}`);
        }

        clearDocumentList();

    } catch (error) {

        console.error("Error deleting all documents:", error);

    }
});

function clearDocumentList() {

    documentList.innerHTML = "";

}

// ============================================================
// Models
// ============================================================

async function loadModels() {

    try {

        const response = await fetch("/api/models");

        if (!response.ok) {
            throw new Error(`Failed to load models: ${response.status}`);
        }

        const data = await response.json();

        const modelSelect = document.querySelector("#model");

        modelSelect.innerHTML = "";

        for (const model of data.models) {

            const option = document.createElement("option");

            option.value = model;
            option.textContent = model;

            if (model === data.current_model) {
                option.selected = true;
            }

            modelSelect.appendChild(option);
        }

    } catch (error) {

        console.error("Error loading models:", error);

    }
}


// ============================================================
// Settings
// ============================================================

const settingsForm = document.querySelector("#settings-form");


settingsForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const model = document.querySelector("#model").value;

    try {

        const response = await fetch("/api/settings/model", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                model: model
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to change model: ${response.status}`);
        }

        const data = await response.json();

        console.log("Model changed:", data.current_model);

    } catch (error) {

        console.error("Error changing model:", error);

    }
});


// ============================================================
// PDF Upload
// ============================================================

const fileInput = document.getElementById("pdf-files");


fileInput.addEventListener("change", async () => {

    if (fileInput.files.length === 0) {
        return;
    }

    const formData = new FormData();

    for (const file of fileInput.files) {

        formData.append("pdf_files", file);

    }

    try {

        console.log("Uploading files...");

        const response = await fetch("/upload", {

            method: "POST",

            body: formData

        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.status}`);
        }

        const data = await response.json();

        console.log("Upload response:", data);

        // Reload the entire page
        window.location.reload();

    } catch (error) {

        console.error("Upload error:", error);

    }
});


// ============================================================
// Chat
// ============================================================

const questionForm = document.getElementById("question-form");
const questionInput = document.getElementById("question-input");

// must be a DOM element, not a <p> tag, to allow appending messages
const conversationMessages = document.getElementById("conversation-messages");

questionForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    console.log("QUESTION FORM SUBMITTED");

    const question = questionInput.value.trim();

    console.log("Question:", question);

    if (!question) {
        return;
    }

    addMessage("user", question);

    questionInput.value = "";

    try {

        console.log("Sending request to /api/chat...");

        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        console.log("API response status:", response.status);

        if (!response.ok) {
            throw new Error(`Chat request failed: ${response.status}`);
        }

        const data = await response.json();

        console.log("API response:", data);

        addMessage("assistant", data.answer);

    } catch (error) {

        console.error("Chat error:", error);

        addMessage(
            "assistant",
            "An error occurred while contacting the AI."
        );
    }
});

function addMessage(role, content) {

    const messageElement = document.createElement("div");

    messageElement.className = `message ${role}`;

    messageElement.innerHTML = `
        <div class="message-role">
            ${role === "user" ? "You" : "AI"}
        </div>

        <div class="message-content">
            ${escapeHtml(content)}
        </div>
    `;

    conversationMessages.appendChild(messageElement);

    conversationMessages.scrollTop =
        conversationMessages.scrollHeight;
}

async function loadConversation() {

    try {

        const response = await fetch("/api/conversation");

        if (!response.ok) {
            throw new Error("Failed to load conversation");
        }

        const conversation = await response.json();

        conversationMessages.innerHTML = "";

        const count = Math.max(
            conversation.questions.length,
            conversation.answers.length
        );

        for (let i = 0; i < count; i++) {

            if (conversation.questions[i]) {
                addMessage(
                    "user",
                    conversation.questions[i]
                );
            }

            if (conversation.answers[i]) {
                addMessage(
                    "assistant",
                    conversation.answers[i]
                );
            }
        }

    } catch (error) {

        console.error(
            "Error loading conversation:",
            error
        );
    }
}


// ============================================================
// Initial page loading
// ============================================================

loadDocuments();

loadModels();

loadConversation();