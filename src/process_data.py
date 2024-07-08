"""データを前処理するスクリプト"""

import json
import os

from type import AbbreviationBase

os.chdir(os.path.dirname(os.path.abspath(__file__)))


base_json_data = json.load(open("./data/abbreviation-base.json", "r"))
if not isinstance(base_json_data, list):
    raise ValueError("略語データがリストでない")
data: list[AbbreviationBase] = []
for item in base_json_data:
    model = AbbreviationBase.model_validate(item)
    data.append(model)

# TODO: データの加工処理を行う
