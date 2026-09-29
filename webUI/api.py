from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from python_core.ai.AIManager import AIManager
from python_core.pdf.PdfList import PdfList
from python_core.pdf.PdfManager import PdfManager


# ============================================================
# Configuration
# ============================================================

MODEL = "lfm2.5-local"

PDF_DIRECTORY = Path("./pdf_files")
PARSED_DOCUMENT_DIRECTORY = Path("./python_core/parsed_doc")

PDF_DIRECTORY.mkdir(parents=True, exist_ok=True)
PARSED_DOCUMENT_DIRECTORY.mkdir(parents=True, exist_ok=True)

app = FastAPI()

ai = AIManager(MODEL)
PDF_MANAGER = PdfManager()

# ============================================================
# Static files
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="webUI/static"),
    name="static"
)


# ============================================================
# Web UI
# ============================================================

@app.get("/")
def home():
    return FileResponse("webUI/templates/index.html")


# ============================================================
# Chat
# ============================================================

class ChatRequest(BaseModel):
    question: str


@app.post("/api/chat")
def chat(request: ChatRequest):

    response = ai.ask(request.question)

    return {
        "response": response
    }


# ============================================================
# Documents
# ============================================================

@app.get("/api/documents")
def get_documents():

    documents = []

    for pdf_path in PDF_DIRECTORY.glob("*.pdf"):

        documents.append({
            "name": pdf_path.name,
            "pages": 0
        })

    return documents


# ============================================================
# Upload PDFs
# ============================================================

@app.post("/upload")
async def upload(pdf_files: list[UploadFile] = File(...)):

    pdf_paths = []

    # save uploaded PDF files to the specified directory
    for pdf_file in pdf_files:

        if not pdf_file.filename:
            continue

        file_location = PDF_DIRECTORY / pdf_file.filename

        with open(file_location, "wb") as f:
            f.write(await pdf_file.read())

        pdf_paths.append(str(file_location))

    if not pdf_paths:
        return {
            "files": []
        }

    # create a PdfList instance with the uploaded PDF paths
    pdf_list = PdfList(pdf_paths)

    # parse all PDFs and generate JSON files
    documents = PDF_MANAGER.parse_all(pdf_list)

    # clean up document names to only include the file name without the path
    for document in documents:
        document.name = Path(document.name).name

    # save the parsed documents as JSON files in the specified directory
    PDF_MANAGER.to_json_all(
        documents,
        str(PARSED_DOCUMENT_DIRECTORY)
    )

    # finding the uploaded files that have a filename and returning their names (useful for the frontend to display the uploaded files)
    return {
        "files": [
            pdf_file.filename
            for pdf_file in pdf_files
            if pdf_file.filename
        ]
    }


# ============================================================
# Models
# ============================================================

@app.get("/api/models")
def get_models():

    return {
        "models": ai.all_models,
        "current_model": ai.current_model
    }


class ModelRequest(BaseModel):
    model: str


@app.post("/api/settings/model")
def set_model(request: ModelRequest):

    if request.model not in ai.all_models:
        return {
            "success": False,
            "error": "Unknown model"
        }

    ai.set_model(request.model)

    return {
        "success": True,
        "current_model": ai.current_model
    }