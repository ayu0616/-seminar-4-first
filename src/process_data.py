"""データを前処理するスクリプト"""

import json
import os

import pykakasi

from type import SOKUON, SYLLABIC_NASAL, Abbreviation, AbbreviationBase, Element, Mora, Syllable

VOWELS = {"a", "e", "i", "o", "u"}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Converter:
    def __init__(self):
        self.kakasi = pykakasi.kakasi()
        self.kakasi.setMode("H", "a")
        self.kakasi.setMode("K", "a")
        self.converter = self.kakasi.getConverter()
        pre_conv_dict = {
            "ティ": "thi",
            "ディ": "dhi",
            "トゥ": "twu",
            "ドゥ": "dwu",
            "チェ": "che",
            "ジェ": "je",
            "シェ": "she",
            "ツァ": "tsa",
            "ツィ": "tsi",
            "ツェ": "tse",
            "ツォ": "tso",
            "ファ": "fa",
            "フィ": "fi",
            "フェ": "fe",
            "フォ": "fo",
            "ウィ": "wi",
            "ウェ": "we",
            "ウォ": "wo",
            "ヴァ": "va",
            "ヴィ": "vi",
            "ヴェ": "ve",
            "ヴォ": "vo",
            "グァ": "gwa",
            "グィ": "gwi",
            "グェ": "gwe",
            "グォ": "gwo",
        }
        self.pre_conv_dict = pre_conv_dict

    def do(self, text: str) -> str:
        text = self._pre_convert(text)
        return self.converter.do(text)

    def _pre_convert(self, text: str) -> str:
        for k, v in self.pre_conv_dict.items():
            k1 = f"{k}ー"
            v1 = f"{v}{v[-1]}"
            text = text.replace(k1, v1)
            text = text.replace(k, v)
        return text


conv = Converter()

base_json_data = json.load(open("./data/abbreviation-base.json", "r"))
if not isinstance(base_json_data, list):
    raise ValueError("略語データがリストでない")
data: list[AbbreviationBase] = list(map(AbbreviationBase.model_validate, base_json_data))


def roman_to_mora_list(roman: str) -> list[Mora]:
    mora_list: list[Mora] = []
    consonant = ""
    for char in roman:
        if char in VOWELS:
            if consonant == "tch":
                mora_list.append(SOKUON)
                mora_list.append(Mora(vowel=char, consonant="ch"))
            else:
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


def mora_list_to_syllable_list(mora_list: list[Mora]) -> list[Syllable]:
    syllable_list: list[Syllable] = []
    for mora in mora_list:
        if mora.is_special():
            syllable_list[-1].coda.append(mora.consonant)
        elif mora.consonant == "" and len(syllable_list) > 0 and syllable_list[-1].syllabic[-1] == mora.vowel:
            syllable_list[-1].syllabic.append(mora.vowel)
        else:
            syllable_list.append(Syllable(onset=[mora.consonant], syllabic=[mora.vowel], coda=[]))
    return syllable_list


def word_to_element_list(word: str) -> list[Element]:
    element_list: list[Element] = []
    for elem_str in word.split("・"):
        roman = conv.do(elem_str)
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
