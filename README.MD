# PDF AI

A lightweight local AI application for interacting with PDF documents.

PDF AI allows you to upload PDF documents, parse their content, store the parsed data as JSON, and ask a local LLM questions about the uploaded documents through a simple web interface.

The project is intentionally built without a frontend framework such as React. The web interface uses standard HTML, CSS and JavaScript, while FastAPI provides the backend API.

The AI runs locally through Ollama, so documents and conversations can remain on the local machine.

## Features

* Upload one or multiple PDF documents
* Automatically parse uploaded PDFs
* Store parsed documents as JSON
* Display uploaded documents in the web interface
* Delete individual documents
* Delete all documents
* Ask questions about the available documents
* Use a local LLM through Ollama
* Select the active AI model from the web interface
* Simple responsive web interface
* No Node.js or npm required

## Architecture

The current architecture is intentionally simple:

```text
PDF_AI/
│
├── main.py
│
├── pdf_files/
│   └── Uploaded PDF files
│
├── python_core/
│   │
│   ├── ai/
│   │   ├── python files
│   │   └── ...
│   │
│   ├── pdf/
│   │   ├── python files
│   │   └── ...
│   │
│   └── parsed_doc/
│       └── Parsed document JSON files
│
├── webUI/
│   │
│   ├── api.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── script.js
│
├── Modelfile
├── requirements.txt
└── README.md
```

## How it works

When a PDF is uploaded through the web interface, the following pipeline is used:

```text
PDF upload
    │
    ▼
FastAPI
    │
    ▼
pdf_files/
    │
    ▼
PdfList
    │
    ▼
PdfManager
    │
    ▼
PDF parsing
    │
    ▼
parsed_doc/*.json
    │
    ▼
AIManager
    │
    ▼
Ollama
    │
    ▼
Local LLM response
```

The parsed JSON documents are used as the source of context for the AI.

At the current stage, the AI can use the available parsed documents directly as context. A more advanced retrieval system / RAG pipeline is planned for a future versions.

# Installation

## Requirements

You need:

* Python 3.13 or a compatible recent Python version
* Ollama

Node.js and npm are not required.

## 1. Clone the repository

```bash
git clone <repository-url>
cd PDF_AI
```

## 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## 4. Install Ollama

Install Ollama for your operating system and make sure the Ollama service is running.

The application currently expects the following model :

```text
lfm2.5-local
```
(Expect changes later to add new models easily but currently it's not available)

The model is created locally from the provided `Modelfile`.

To help you through the installation you can also run the python script "model_installer.py"

From the project root:

```bash
ollama create lfm2.5-local -f Modelfile
```

You can verify that the model was successfully installed with:

```bash
ollama list
```

You should see something similar to:

```text
NAME                   ID              SIZE
lfm2.5-local:latest    ...             ...
```

# Running the application

Make sure your virtual environment is activated.

From the project root:

```bash
uvicorn webUI.api:app --reload
```

The server should start on:

```text
http://127.0.0.1:8000
```

Open this address in your browser.

# Using the application

## Uploading documents

In the Documents panel, click:

```text
+ Select PDFs
```

You can select one or multiple PDF files.

The files are automatically uploaded and parsed.

The original PDFs are stored in:

```text
pdf_files/
```

The parsed representations are stored in:

```text
python_core/parsed_doc/
```

## Asking questions

Enter a question in the Conversation panel and click `Send` or enter.

# Project status

Current version: **V1**

The current version focuses on having a complete end-to-end working pipeline rather than a highly polished interface or optimized AI system.

The main workflow is functional:

```text
Upload PDF
     ↓
Parse PDF
     ↓
Generate JSON
     ↓
Store document
     ↓
Build AI context
     ↓
Ask question
     ↓
Ollama
     ↓
Display response
```

# Planned improvements

Several improvements are planned for future versions.

### Better document retrieval

Currently, the AI can receive a large amount of document context.

A future version will implement a retrieval system so that the application can identify the relevant pages or passages before querying the model.

```text
Question
   ↓
Document search
   ↓
Relevant pages/passages
   ↓
Reduced context
   ↓
LLM
   ↓
Answer
```

This should reduce unnecessary context and improve response quality, especially when many or large documents are loaded.

### Better source references

The AI currently receives document and page information, but source citation accuracy can still be improved.

The goal is to provide reliable references such as:

```text
[ResumeX.pdf, page 1]
```

based on the actual retrieved content.

### Conversation history

The current implementation handles individual questions.

A future version can add persistent conversation history so that follow-up questions can refer to previous messages.

### Improved UI

The current frontend intentionally uses plain HTML, CSS and JavaScript.

Future versions may improve:

* document management
* conversation display
* loading states
* error messages
* model management
* document selection
* mobile layout

# Development

Start the development server with:

```bash
uvicorn webUI.api:app --reload
```

The `--reload` option automatically restarts the server when Python files are modified.

## Frontend

The frontend does not require a build system.

Changes to HTML, CSS and JavaScript can therefore be tested directly by refreshing the browser.

# Git

Generated/local files should not be committed to the repository.

In particular, parsed documents and locally stored models should remain outside Git:

```gitignore
python_core/parsed_doc/*
models/lfm2.5/*
pdf_files/*
```

The exact Git configuration may vary depending on which sample files or resources are intentionally included in the repository.

# License

This project is currently a personal development project.