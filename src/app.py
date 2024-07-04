import json
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier

from model.sequential_classfier import SequentialClassifier
from mora_wakati import mora_wakati
from process_data import processing
from type.abbreviation import Abbreviation, AbbreviationBase
from type.features import CrfFeatures, CrfLabel, CrfLabelSequence

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()


class Input(BaseModel):
    words: list[list[str]]
    rank_n: int = 1


class Abbrs(BaseModel):
    abbrs: list[list[str]]


# 前処理した略語データを読み込む
data = list(map(Abbreviation.model_validate, json.load(open("./data/abbreviation.json", "r"))))
X = [*map(CrfFeatures.from_abbreviation, data)]
y = list(map(CrfLabelSequence.from_abbreviation, data))
# ラベルの番号振り
CrfFeatures.assign_feature_idx(X)
model = SequentialClassifier(
    RandomForestClassifier(
        random_state=616,
        n_estimators=393,
        max_depth=19,
        max_features="sqrt",
        criterion="entropy",
    )
)
model.fit(X, y)


@app.post("/api", response_model=Abbrs)
async def api(input_data: Input):
    words = input_data.words
    rank_n = input_data.rank_n

    data = [processing(AbbreviationBase(word="・".join(filter(bool, word)), abbreviation="")) for word in words]
    X = [*map(CrfFeatures.from_abbreviation, data)]
    abbrs: list[list[str]] = []
    for i, abbr in enumerate(model.predict_rank(X, rank_n)):
        word = data[i].word.replace("・", "")
        word_moras = mora_wakati(word)
        assert len(word_moras) == len(abbr[0])
        print(abbr[0])
        abbrs.append(["".join([m for lb, m in zip(labels, word_moras) if CrfLabel.is_abbr(lb)]) for labels in abbr])

    return Abbrs(abbrs=abbrs)


@app.get("/")
async def index():
    return FileResponse("./web/dist/index.html")


@app.get("/{path:path}")
async def web_path(path: str):
    return FileResponse(f"./web/dist/{path}")
