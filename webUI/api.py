from fastapi import FastAPI
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