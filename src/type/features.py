from typing import ClassVar, Iterable

from pydantic import BaseModel

from type import Abbreviation
from type.phoneme import Mora


class CrfLabel(BaseModel):
    NG: ClassVar[str] = "NG"
    B_ABBR: ClassVar[str] = "B-Abbr"
    I_ABBR: ClassVar[str] = "I-Abbr"
    E_ABBR: ClassVar[str] = "E-Abbr"

    @staticmethod
    def is_abbr(label: str) -> bool:
        return label in {CrfLabel.B_ABBR, CrfLabel.I_ABBR, CrfLabel.E_ABBR}


crf_label = CrfLabel()


class CrfFeatures(BaseModel):
    BOS: ClassVar[str] = "BOS"
    EOS: ClassVar[str] = "EOS"
    to_int_idx: ClassVar[dict[str, int]] = {}
    no_use_keys: ClassVar[Iterable[str]] = []

    # モーラ
    vowel: str
    consonant: str
    mora: str

    # 1つ前
    prev1_vowel: str
    prev1_consonant: str
    prev1_mora: str
    # 2つ前
    prev2_vowel: str
    prev2_consonant: str
    prev2_mora: str
    # 3つ前
    prev3_vowel: str
    prev3_consonant: str
    prev3_mora: str

    # 略語の1つ前のモーラ
    prev_abbr_vowel: str = ""
    prev_abbr_consonant: str = ""
    prev_abbr_mora: str = ""

    # 1つ後
    next1_vowel: str
    next1_consonant: str
    next1_mora: str
    # 2つ後
    next2_vowel: str
    next2_consonant: str
    next2_mora: str
    # 3つ後
    next3_vowel: str
    next3_consonant: str
    next3_mora: str

    is_syllabic_nasal: bool  # 撥音かどうか
    is_sokuon: bool  # 促音かどうか
    is_long: bool  # 長音かどうか

    next_is_syllabic_nasal: bool  # 次が撥音かどうか
    next_is_sokuon: bool  # 次が促音かどうか
    next_is_long: bool  # 次が長音かどうか
    prev_is_syllabic_nasal: bool  # 前が撥音かどうか
    prev_is_sokuon: bool  # 前が促音かどうか
    prev_is_long: bool  # 前が長音かどうか

    # 要素
    elem_num: int  # 何番目の要素か
    mora_num: int  # 何番目のモーラか
    elem_len: int  # 単語全体の要素数
    mora_len_in_elem: int  # 要素全体のモーラ数
    total_mora_len: int  # 単語全体のモーラ数
    begin_of_elem: bool  # 要素の先頭かどうか
    end_of_elem: bool  # 要素の末尾かどうか

    current_mora_len: int = 0  # 現在までに採用されたモーラ数（学習の過程で求める）

    def get_array(self):
        """特徴量配列を取得する"""
        return [f"{k}={v}" for k, v in self.model_dump().items()]

    @classmethod
    def from_abbreviation(cls, abbr: Abbreviation) -> list["CrfFeatures"]:
        """略語から特徴量のリストを生成する"""
        res: list["CrfFeatures"] = []
        elem_len = len(abbr.word_element_list)
        total_mora_len = sum([len(e.mora_list) for e in abbr.word_element_list])
        for i, elem in enumerate(abbr.word_element_list):
            mora_len_in_elem = len(elem.mora_list)
            for j, feat_list in enumerate(elem.mora_list):
                if j == mora_len_in_elem - 1:
                    next1_vowel = cls.EOS
                    next1_consonant = cls.EOS
                    next2_vowel = cls.EOS
                    next2_consonant = cls.EOS
                    next3_vowel = cls.EOS
                    next3_consonant = cls.EOS
                elif j == mora_len_in_elem - 2:
                    next1_vowel = elem.mora_list[j + 1].vowel
                    next1_consonant = elem.mora_list[j + 1].consonant
                    next2_vowel = cls.EOS
                    next2_consonant = cls.EOS
                    next3_vowel = cls.EOS
                    next3_consonant = cls.EOS
                elif j == mora_len_in_elem - 3:
                    next1_vowel = elem.mora_list[j + 1].vowel
                    next1_consonant = elem.mora_list[j + 1].consonant
                    next2_vowel = elem.mora_list[j + 2].vowel
                    next2_consonant = elem.mora_list[j + 2].consonant
                    next3_vowel = cls.EOS
                    next3_consonant = cls.EOS
                else:
                    next1_vowel = elem.mora_list[j + 1].vowel
                    next1_consonant = elem.mora_list[j + 1].consonant
                    next2_vowel = elem.mora_list[j + 2].vowel
                    next2_consonant = elem.mora_list[j + 2].consonant
                    next3_vowel = elem.mora_list[j + 3].vowel
                    next3_consonant = elem.mora_list[j + 3].consonant
                if j == 0:
                    prev1_vowel = cls.BOS
                    prev1_consonant = cls.BOS
                    prev2_vowel = cls.BOS
                    prev2_consonant = cls.BOS
                    prev3_vowel = cls.BOS
                    prev3_consonant = cls.BOS
                elif j == 1:
                    prev1_vowel = elem.mora_list[j - 1].vowel
                    prev1_consonant = elem.mora_list[j - 1].consonant
                    prev2_vowel = cls.BOS
                    prev2_consonant = cls.BOS
                    prev3_vowel = cls.BOS
                    prev3_consonant = cls.BOS
                else:
                    prev1_vowel = elem.mora_list[j - 1].vowel
                    prev1_consonant = elem.mora_list[j - 1].consonant
                    prev2_vowel = elem.mora_list[j - 2].vowel
                    prev2_consonant = elem.mora_list[j - 2].consonant
                    prev3_vowel = elem.mora_list[j - 3].vowel
                    prev3_consonant = elem.mora_list[j - 3].consonant
                next_is_syllabic_nasal = j < mora_len_in_elem - 1 and elem.mora_list[j + 1].is_syllabic_nasal()
                prev_is_syllabic_nasal = j > 0 and elem.mora_list[j - 1].is_syllabic_nasal()
                next_is_sokuon = j < mora_len_in_elem - 1 and elem.mora_list[j + 1].is_sokuon()
                prev_is_sokuon = j > 0 and elem.mora_list[j - 1].is_sokuon()
                is_long = prev1_vowel == feat_list.vowel and feat_list.consonant == ""
                next_is_long = next1_vowel == feat_list.vowel and next1_consonant == ""
                prev_is_long = prev1_vowel == prev2_vowel and prev1_consonant == ""
                res.append(
                    cls(
                        vowel=feat_list.vowel,
                        consonant=feat_list.consonant,
                        mora=feat_list.consonant + feat_list.vowel,
                        prev1_vowel=prev1_vowel,
                        prev1_consonant=prev1_consonant,
                        prev1_mora=prev1_consonant + prev1_vowel,
                        next1_vowel=next1_vowel,
                        next1_consonant=next1_consonant,
                        next1_mora=next1_consonant + next1_vowel,
                        prev2_vowel=prev2_vowel,
                        prev2_consonant=prev2_consonant,
                        prev2_mora=prev2_consonant + prev2_vowel,
                        next2_vowel=next2_vowel,
                        next2_consonant=next2_consonant,
                        next2_mora=next2_consonant + next2_vowel,
                        prev3_vowel=prev3_vowel,
                        prev3_consonant=prev3_consonant,
                        prev3_mora=prev3_consonant + prev3_vowel,
                        next3_vowel=next3_vowel,
                        next3_consonant=next3_consonant,
                        next3_mora=next3_consonant + next3_vowel,
                        elem_num=i,
                        mora_num=j,
                        elem_len=elem_len,
                        mora_len_in_elem=mora_len_in_elem,
                        is_syllabic_nasal=feat_list.is_syllabic_nasal(),
                        is_sokuon=feat_list.is_sokuon(),
                        is_long=is_long,
                        next_is_syllabic_nasal=next_is_syllabic_nasal,
                        next_is_sokuon=next_is_sokuon,
                        next_is_long=next_is_long,
                        prev_is_syllabic_nasal=prev_is_syllabic_nasal,
                        prev_is_sokuon=prev_is_sokuon,
                        prev_is_long=prev_is_long,
                        total_mora_len=total_mora_len,
                        begin_of_elem=j == 0,
                        end_of_elem=j == mora_len_in_elem - 1,
                    )
                )
        return res

    @staticmethod
    def assign_feature_idx(X: list[list["CrfFeatures"]]):
        """特徴量のインデックスを割り当てる"""
        if len(CrfFeatures.to_int_idx) > 0:
            # to_int_idxが空でない場合はエラーを出す（割り当て済みなので）
            raise Exception("CrfFeatures.to_int_idx is not empty")
        CrfFeatures.to_int_idx = {CrfLabel.__dict__[v]: i for i, v in enumerate(CrfLabel.__class_vars__)}
        vowels = {"a", "i", "u", "e", "o"}
        consonants = {mora.consonant for word in X for mora in word} - {"N", "Q"}
        feat_keys = {"prev1", "prev2", "prev3", "next1", "next2", "next3", "prev_abbr"}

        # ダミーデータのインデックス
        for v in vowels:
            for c in consonants:
                for k in feat_keys:
                    feats = [f"{k}_vowel={v}", f"{k}_consonant={c}", f"{k}_mora={c}{v}"]
                    for feat in feats:
                        if feat not in CrfFeatures.to_int_idx:
                            CrfFeatures.to_int_idx[feat] = len(CrfFeatures.to_int_idx)
                feats = [f"vowel={v}", f"consonant={c}", f"mora={c}{v}"]
                for feat in feats:
                    if feat not in CrfFeatures.to_int_idx:
                        CrfFeatures.to_int_idx[feat] = len(CrfFeatures.to_int_idx)
        for k in feat_keys:
            bos_feats = [f"{k}_vowel={CrfFeatures.BOS}", f"{k}_consonant={CrfFeatures.BOS}", f"{k}_mora={CrfFeatures.BOS}{CrfFeatures.BOS}"]
            eos_feats = [f"{k}_vowel={CrfFeatures.EOS}", f"{k}_consonant={CrfFeatures.EOS}", f"{k}_mora={CrfFeatures.EOS}{CrfFeatures.EOS}"]
            nasal_feats = [f"{k}_vowel=", f"{k}_consonant=N", f"{k}_mora=N"]
            sokuon_feats = [f"{k}_vowel=", f"{k}_consonant=Q", f"{k}_mora=Q"]
            empty_feats = [f"{k}_mora="]
            feats = bos_feats + eos_feats + nasal_feats + sokuon_feats + empty_feats
            for feat in feats:
                if feat not in CrfFeatures.to_int_idx:
                    CrfFeatures.to_int_idx[feat] = len(CrfFeatures.to_int_idx)
        bos_feats = [f"vowel={CrfFeatures.BOS}", f"consonant={CrfFeatures.BOS}", f"mora={CrfFeatures.BOS}{CrfFeatures.BOS}"]
        eos_feats = [f"vowel={CrfFeatures.EOS}", f"consonant={CrfFeatures.EOS}", f"mora={CrfFeatures.EOS}{CrfFeatures.EOS}"]
        nasal_feats = ["vowel=", "consonant=N", "mora=N"]
        sokuon_feats = ["vowel=", "consonant=Q", "mora=Q"]
        feats = bos_feats + eos_feats + nasal_feats + sokuon_feats
        for feat in feats:
            if feat not in CrfFeatures.to_int_idx:
                CrfFeatures.to_int_idx[feat] = len(CrfFeatures.to_int_idx)

        # 数値データのインデックス
        for word in X:
            for mora in word:
                for k, v in mora.model_dump().items():
                    if type(v) in {int, float, bool}:
                        feat = k
                    if feat not in CrfFeatures.to_int_idx:
                        CrfFeatures.to_int_idx[feat] = len(CrfFeatures.to_int_idx)

    @staticmethod
    def get_numbered_features(X: list[list["CrfFeatures"]]) -> list[list[list[float]]]:
        """特徴量を数値化する"""
        no_use_keys = set(CrfFeatures.no_use_keys)
        for k in no_use_keys:
            if k not in X[0][0].model_dump():
                raise ValueError(f"key {k} is not in CrfFeatures")
        res: list[list[list[float]]] = []
        for word in X:
            res_word: list[list[float]] = []
            for mora in word:
                res_mora: list[float] = [0.0] * len(CrfFeatures.to_int_idx)
                for k, v in mora.model_dump().items():
                    if k in no_use_keys:
                        continue
                    match v:
                        case int() | float():
                            idx = CrfFeatures.to_int_idx[k]
                            res_mora[idx] = v
                        case bool():
                            idx = CrfFeatures.to_int_idx[k]
                            res_mora[idx] = 1 if v else 0
                        case _:
                            feat = f"{k}={v}"
                            idx = CrfFeatures.to_int_idx[feat]
                            res_mora[idx] = 1
                res_word.append(res_mora)
            res.append(res_word)
        return res


class CrfLabelSequence(list[str]):
    def __init__(self, data: list[str] = [], abbr_mora_list: list[Mora] = []):
        super().__init__(data)
        self.abbr_mora_list = abbr_mora_list

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
        return cls(res, abbr_mora_list)
