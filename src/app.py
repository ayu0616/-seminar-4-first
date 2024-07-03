import os
import random

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()


class Input(BaseModel):
    words: list[list[str]]
    rank_n: int = 1


class Abbrs(BaseModel):
    abbrs: list[list[str]]


@app.post("/api", response_model=Abbrs)
async def api(input_data: Input):
    words = input_data.words
    rank_n = input_data.rank_n

    abbrs: list[list[str]] = []
    for word_list in words:
        word = "".join(word_list)
        li: list[str] = []
        for i in range(rank_n):
            w = ""
            for c in word:
                if random.random() < 0.5:
                    w += c
            li.append(w)
        abbrs.append(li)

    return Abbrs(abbrs=abbrs)


@app.get("/")
async def index():
    return FileResponse("./web/dist/index.html")


@app.get("/{path:path}")
async def web_path(path: str):
    return FileResponse(f"./web/dist/{path}")
