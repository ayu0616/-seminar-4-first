"""データを前処理するスクリプト"""

import json
import os

import pykakasi

from type import SOKUON, SYLLABIC_NASAL, Abbreviation, AbbreviationBase, Element, Mora, Syllable

VOWELS = {"a", "e", "i", "o", "u"}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

kakasi = pykakasi.kakasi()

base_json_data = json.load(open("./data/abbreviation-base.json", "r"))
if not isinstance(base_json_data, list):
    raise ValueError("略語データがリストでない")
data: list[AbbreviationBase] = list(map(AbbreviationBase.model_validate, base_json_data))


def roman_to_mora_list(roman: str) -> list[Mora]:
    mora_list: list[Mora] = []
    consonant = ""
    for char in roman:
        if char in VOWELS:
            mora_list.append(Mora(vowel=char, consonant=consonant))
            consonant = ""
        elif consonant == "n" and char != "y":
            mora_list.append(SYLLABIC_NASAL)
            consonant = "" if char == "'" else char
        elif consonant == char:
            mora_list.append(SOKUON)
            consonant = char
        else:
            consonant += char
    if consonant == "n":
        mora_list.append(SYLLABIC_NASAL)
    return mora_list


def mora_list_to_syllable_list(mora_list: list[Mora]) -> list[Syllable]:  # TODO: 頑張る
    syllable_list: list[Syllable] = [Syllable()]
    for mora in mora_list:
        if mora.vowel == "":
            syllable_list[-1].coda.append(mora.consonant)
            syllable_list.append(Syllable())
        else:
            syllable_list[-1].onset.append(mora.consonant)
            syllable_list[-1].syllabic.append(mora.vowel)
    return syllable_list


def word_to_element_list(word: str) -> list[Element]:
    element_list: list[Element] = []
    for elem_str in word.split("・"):
        roman = kakasi.convert(elem_str)[0]["hepburn"]
        mora_list = roman_to_mora_list(roman)
        syllable_list = mora_list_to_syllable_list(mora_list)
        element = Element(text=elem_str, mora_list=mora_list, syllable_list=syllable_list)
        element_list.append(element)
    return element_list


def processing(base_data: AbbreviationBase) -> Abbreviation:
    word_elem_list = word_to_element_list(base_data.word)
    abbr_elem_list = word_to_element_list(base_data.abbreviation)
    abbr = Abbreviation(
        word=base_data.word,
        abbreviation=base_data.abbreviation,
        word_element_list=word_elem_list,
        abbreviation_element_list=abbr_elem_list,
    )
    return abbr


processed_data = list(map(processing, data))

json.dump([d.model_dump() for d in processed_data], open("./data/abbreviation.json", "w"), ensure_ascii=False, indent=4)
