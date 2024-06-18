from typing import ClassVar

from pydantic import BaseModel

from type import Abbreviation


class CrfLabel(BaseModel):
    NG: str = "NG"
    B_ABBR: str = "B-Abbr"
    I_ABBR: str = "I-Abbr"
    E_ABBR: str = "E-Abbr"


crf_label = CrfLabel()


class CrfFeatures(BaseModel):
    BOS: ClassVar[str] = "BOS"
    EOS: ClassVar[str] = "EOS"
    to_int_idx: ClassVar[dict[str, int]] = {v: i for i, v in enumerate(crf_label.model_dump().values())}

    # モーラ
    vowel: str
    consonant: str

    # 1つ前
    prev1_vowel: str
    prev1_consonant: str
    # 2つ前
    prev2_vowel: str
    prev2_consonant: str

    # 1つ後
    next1_vowel: str
    next1_consonant: str
    # 2つ後
    next2_vowel: str
    next2_consonant: str

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
            for j, feat_list in enumerate(elem.mora_list):
                if j == mora_len_in_elem - 1:
                    next1_vowel = cls.EOS
                    next1_consonant = cls.EOS
                    next2_vowel = cls.EOS
                    next2_consonant = cls.EOS
                elif j == mora_len_in_elem - 2:
                    next1_vowel = elem.mora_list[j + 1].vowel
                    next1_consonant = elem.mora_list[j + 1].consonant
                    next2_vowel = cls.EOS
                    next2_consonant = cls.EOS
                else:
                    next1_vowel = elem.mora_list[j + 1].vowel
                    next1_consonant = elem.mora_list[j + 1].consonant
                    next2_vowel = elem.mora_list[j + 2].vowel
                    next2_consonant = elem.mora_list[j + 2].consonant
                if j == 0:
                    prev1_vowel = cls.BOS
                    prev1_consonant = cls.BOS
                    prev2_vowel = cls.BOS
                    prev2_consonant = cls.BOS
                elif j == 1:
                    prev1_vowel = elem.mora_list[j - 1].vowel
                    prev1_consonant = elem.mora_list[j - 1].consonant
                    prev2_vowel = cls.BOS
                    prev2_consonant = cls.BOS
                else:
                    prev1_vowel = elem.mora_list[j - 1].vowel
                    prev1_consonant = elem.mora_list[j - 1].consonant
                    prev2_vowel = elem.mora_list[j - 2].vowel
                    prev2_consonant = elem.mora_list[j - 2].consonant
                res.append(
                    cls(
                        vowel=feat_list.vowel,
                        consonant=feat_list.consonant,
                        prev1_vowel=prev1_vowel,
                        prev1_consonant=prev1_consonant,
                        next1_vowel=next1_vowel,
                        next1_consonant=next1_consonant,
                        prev2_vowel=prev2_vowel,
                        prev2_consonant=prev2_consonant,
                        next2_vowel=next2_vowel,
                        next2_consonant=next2_consonant,
                        elem_num=i,
                        mora_num=j,
                        elem_len=elem_len,
                        mora_len_in_elem=mora_len_in_elem,
                        is_syllabic_nasal=feat_list.is_syllabic_nasal(),
                        is_sokuon=feat_list.is_sokuon(),
                    )
                )
        # 特徴量のインデックスを取得
        for feat_list in res:
            for k, v in feat_list.model_dump().items():
                if type(v) in {int, float, bool}:
                    feat = k
                else:
                    feat = f"{k}={v}"
                if feat not in CrfFeatures.to_int_idx:
                    CrfFeatures.to_int_idx[feat] = len(CrfFeatures.to_int_idx)
        return res

    @staticmethod
    def get_numbered_features(X: list[list["CrfFeatures"]]) -> list[list[list[int]]]:
        """特徴量を数値化する"""
        res: list[list[list[int]]] = []
        for word in X:
            res_word: list[list[int]] = []
            for mora in word:
                res_mora: list[int] = [0] * len(CrfFeatures.to_int_idx)
                for k, v in mora.model_dump().items():
                    if type(v) in {int, float}:
                        idx = CrfFeatures.to_int_idx[k]
                        res_mora[idx] = int(v)
                    elif type(v) is bool:
                        idx = CrfFeatures.to_int_idx[k]
                        res_mora[idx] = 1 if v else 0
                    else:
                        feat = f"{k}={v}"
                        idx = CrfFeatures.to_int_idx[feat]
                        res_mora[idx] = 1
                res_word.append(res_mora)
            res.append(res_word)
        return res


class CrfLabelSequence(list[str]):
    def __init__(self, data: list[str] = []):
        super().__init__(data)

    @classmethod
    def from_abbreviation(cls, abbr: Abbreviation) -> "CrfLabelSequence":
        word_mora_list = [mora for elem in abbr.word_element_list for mora in elem.mora_list]
        abbr_mora_list = [mora for elem in abbr.abbreviation_element_list for mora in elem.mora_list]
        n = len(word_mora_list)
        abbr_n = len(abbr_mora_list)
        abbr_i = 0
        res = [crf_label.NG] * n
        in_abbr = False
        for i in range(n):
            if abbr_i >= abbr_n:
                break
            if word_mora_list[i] == abbr_mora_list[abbr_i]:
                res[i] = crf_label.I_ABBR if in_abbr else crf_label.B_ABBR
                abbr_i += 1
                in_abbr = True
            else:
                in_abbr = False
        for i in range(n - 1):
            if res[i] == crf_label.I_ABBR and res[i + 1] == crf_label.NG:
                res[i] = crf_label.E_ABBR
                # res[i + 1] = crf_label.E_ABBR
        return cls(res)
