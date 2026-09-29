from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from python_core.ai.AIManager import AIManager


app = FastAPI()

ai = AIManager()

app.mount(
    "/static",
    StaticFiles(directory="webUI/static"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("webUI/templates/index.html")


class ChatRequest(BaseModel):
    question: str


@app.post("/api/chat")
def chat(request: ChatRequest):
    response = ai.ask(request.question)

    return {
        "response": response
    }

@app.post("/upload")
async def upload(pdf_files: list[UploadFile] = File(...)):
    for pdf_file in pdf_files:
        file_location = f"pdf_files/{pdf_file.filename}"
        with open(file_location, "wb") as f:
            f.write(await pdf_file.read())