import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()


@app.get("/api")
async def api():
    return {"message": "Hello World"}  # TODO: APIの実装


@app.get("/")
async def index():
    return FileResponse("./web/dist/index.html")


@app.get("/{path:path}")
async def web_path(path: str):
    return FileResponse(f"./web/dist/{path}")
