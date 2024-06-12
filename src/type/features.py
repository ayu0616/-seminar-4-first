from typing import ClassVar

from pydantic import BaseModel

from type import Abbreviation


class CrfFeatures(BaseModel):
    EOS: ClassVar[str] = "EOS"

    # モーラ
    vowel: str
    consonant: str
    next_vowel: str
    next_consonant: str
    is_syllabic_nasal: bool  # 撥音かどうか
    is_sokuon: bool  # 促音かどうか

    # 要素
    elem_num: int  # 何番目の要素か
    mora_num: int  # 何番目のモーラか
    elem_len: int  # 単語全体の要素数
    mora_len_in_elem: int  # 要素全体のモーラ数

    def get_array(self):
        """特徴量配列を取得する"""
        return [f"{k}={v}" for k, v in self.model_dump().items()]

    @classmethod
    def from_abbreviation(cls, abbr: Abbreviation) -> list["CrfFeatures"]:
        """略語から特徴量のリストを生成する"""
        res: list["CrfFeatures"] = []
        elem_len = len(abbr.word_element_list)
        for i, elem in enumerate(abbr.word_element_list):
            mora_len_in_elem = len(elem.mora_list)
            for j, mora in enumerate(elem.mora_list):
                if j == mora_len_in_elem - 1:
                    next_vowel = cls.EOS
                    next_consonant = cls.EOS
                else:
                    next_vowel = elem.mora_list[j + 1].vowel
                    next_consonant = elem.mora_list[j + 1].consonant
                res.append(
                    cls(
                        vowel=mora.vowel,
                        consonant=mora.consonant,
                        next_vowel=next_vowel,
                        next_consonant=next_consonant,
                        elem_num=i,
                        mora_num=j,
                        elem_len=elem_len,
                        mora_len_in_elem=mora_len_in_elem,
                        is_syllabic_nasal=mora.is_syllabic_nasal(),
                        is_sokuon=mora.is_sokuon(),
                    )
                )
        return res


class CrfLabel(list[str]):
    NG = "NG"
    B_ABBR = "B-Abbr"
    I_ABBR = "I-Abbr"

    @classmethod
    def from_abbreviation(cls, abbr: Abbreviation) -> "CrfLabel":
        word_mora_list = [mora for elem in abbr.word_element_list for mora in elem.mora_list]
        abbr_mora_list = [mora for elem in abbr.abbreviation_element_list for mora in elem.mora_list]
        n = len(word_mora_list)
        abbr_n = len(abbr_mora_list)
        abbr_i = 0
        res = [cls.NG] * n
        in_abbr = False
        for i in range(n):
            if abbr_i >= abbr_n:
                break
            if word_mora_list[i] == abbr_mora_list[abbr_i]:
                res[i] = cls.I_ABBR if in_abbr else cls.B_ABBR
                abbr_i += 1
                in_abbr = True
            else:
                in_abbr = False
        return cls(res)
