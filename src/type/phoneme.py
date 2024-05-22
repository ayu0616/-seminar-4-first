from pydantic import BaseModel


class Mora(BaseModel):
    """モーラ"""

    consonant: str  # 子音
    vowel: str  # 母音

    def is_special(self) -> bool:
        """特殊なモーラかどうか"""
        return self in {SYLLABIC_NASAL, SOKUON}

    def __hash__(self) -> int:
        return hash((self.vowel, self.consonant))


SYLLABIC_NASAL = Mora(vowel="", consonant="N")  # 撥音
SOKUON = Mora(vowel="", consonant="Q")  # 促音


class Syllable(BaseModel):
    """音節"""

    onset: list[str] = []  # 音節頭
    syllabic: list[str] = []  # 音節主音
    coda: list[str] = []  # 末尾子音
