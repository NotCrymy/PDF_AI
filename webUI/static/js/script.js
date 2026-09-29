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
    `;

    documentList.appendChild(documentElement);
}


function escapeHtml(text) {

    const element = document.createElement("div");

    element.textContent = text;

    return element.innerHTML;
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

const responseText = document.getElementById("response-text");


questionForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    const question = questionInput.value;

    if (!question.trim()) {
        return;
    }

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        if (!response.ok) {
            throw new Error(`Chat request failed: ${response.status}`);
        }

        const data = await response.json();

        responseText.textContent = data.response;

    } catch (error) {

        console.error("Chat error:", error);

        responseText.textContent = "An error occurred.";

    }
});


// ============================================================
// Initial page loading
// ============================================================

loadDocuments();

loadModels();