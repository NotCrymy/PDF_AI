from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
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


# ============================================================
# Managers
# ============================================================

ai = AIManager(MODEL)
PDF_MANAGER = PdfManager()

# global list containing the currently loaded PDFs
PDF_LIST = PdfList([])


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


@app.delete("/api/documents/{filename}")
def delete_document(filename: str):

    global PDF_LIST

    pdf_path = PDF_DIRECTORY / filename

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # find the corresponding PdfDocument in the global PdfList
    pdf_document = None

    for document in PDF_LIST.list:
        if Path(document.path).name == filename:
            pdf_document = document
            break

    if pdf_document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found in PDF list"
        )

    # delete the PDF + its JSON
    PDF_MANAGER.delete_document(
        pdf_document,
        str(PARSED_DOCUMENT_DIRECTORY)
    )

    # remove the document from the global list
    PDF_LIST.list.remove(pdf_document)

    return {
        "success": True,
        "filename": filename
    }


# ============================================================
# Upload PDFs
# ============================================================

@app.post("/upload")
async def upload(pdf_files: list[UploadFile] = File(...)):

    global PDF_LIST

    pdf_paths = []

    # Save uploaded PDF files to the specified directory
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
    new_pdf_list = PdfList(pdf_paths)

    # parse all PDFs
    documents = PDF_MANAGER.parse_all(new_pdf_list)

    # clean up document names to only include the file name
    for document in documents:
        document.name = Path(document.name).name

    # add the parsed documents to the global PDF list
    PDF_LIST.list.extend(documents)

    # save the parsed documents as JSON files
    PDF_MANAGER.to_json_all(
        documents,
        str(PARSED_DOCUMENT_DIRECTORY)
    )

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