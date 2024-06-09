from pydantic import BaseModel

from type import Abbreviation


class CrfFeatures(BaseModel):
    # モーラ
    vowel: str
    consonant: str
    next_vowel: str
    next_consonant: str

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
        return res


class CrfLabel(list[str]):
    def __init__(self, abbr: Abbreviation):
        super().__init__(abbr.word_element_list)
