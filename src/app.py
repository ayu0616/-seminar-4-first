import json
import os
import pickle
import random

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from model.sequential_classfier import SequentialClassifier
from process_data import processing
from type.abbreviation import Abbreviation, AbbreviationBase
from type.features import CrfFeatures

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

    data = [processing(AbbreviationBase(word="・".join(filter(bool, word)), abbreviation="")) for word in words]
    train_data = list(map(Abbreviation.model_validate, json.load(open("./data/abbreviation.json", "r"))))
    X_train = [*map(CrfFeatures.from_abbreviation, train_data)]
    CrfFeatures.get_numbered_features(X_train)
    X = [*map(CrfFeatures.from_abbreviation, data)]
    model: SequentialClassifier = pickle.load(open("./model.pkl", "rb"))
    abbrs: list[list[str]] = []
    for i, abbr in enumerate(model.predict_rank(X, rank_n)):
        word = data[i].word.replace("・", "")
        print(i, word, abbr)
        abbrs.append(["".join([c for lb, c in zip(labels, word) if lb in {"B-Abbr", "I-Abbr"}]) for labels in abbr])

    return Abbrs(abbrs=abbrs)


@app.get("/")
async def index():
    return FileResponse("./web/dist/index.html")


@app.get("/{path:path}")
async def web_path(path: str):
    return FileResponse(f"./web/dist/{path}")
