from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def home():
    return FileResponse("webUI/templates/index.html")