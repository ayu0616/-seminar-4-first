"""データを前処理するスクリプト"""

import json
import os

import pykakasi

from type import Abbreviation, AbbreviationBase, Element, Mora

os.chdir(os.path.dirname(os.path.abspath(__file__)))

kakasi = pykakasi.kakasi()

base_json_data = json.load(open("./data/abbreviation-base.json", "r"))
if not isinstance(base_json_data, list):
    raise ValueError("略語データがリストでない")
data: list[AbbreviationBase] = list(map(AbbreviationBase.model_validate, base_json_data))


def roman_to_mora_list(roman: str) -> list[Mora]:
    mora_list: list[Mora] = []
    # TODO: ロジックを去年のものから拝借してくる
    for i in range(0, len(roman), 2):
        if i + 1 < len(roman):
            mora = Mora(vowel=roman[i], consonant=roman[i + 1])
        else:
            mora = Mora(vowel=roman[i], consonant="")
        mora_list.append(mora)
    return mora_list


def word_to_element_list(word: str) -> list[Element]:
    element_list: list[Element] = []
    for elem_str in word.split("・"):
        roman = kakasi.convert(elem_str)[0]["hepburn"]
        mora_list = roman_to_mora_list(roman)
        element = Element(text=elem_str, mora_list=mora_list)
        element_list.append(element)
    return element_list


def processing(base_data: AbbreviationBase) -> Abbreviation:
    word_elem_list = word_to_element_list(base_data.word)
    abbr_elem_list = word_to_element_list(base_data.abbreviation)
    abbr = Abbreviation(**base_data.model_dump(), word_element_list=word_elem_list, abbreviation_element_list=abbr_elem_list)
    return abbr


processed_data = list(map(processing, data))

json.dump([d.model_dump() for d in processed_data], open("./data/abbreviation.json", "w"), ensure_ascii=False, indent=4)
