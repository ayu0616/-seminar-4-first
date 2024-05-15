from pydantic import BaseModel


class Mora(BaseModel):
    """モーラ"""

    vowel: str  # 母音
    consonant: str  # 子音


SYLLABIC_NASAL = Mora(vowel="", consonant="N")  # 撥音
SOKUON = Mora(vowel="", consonant="Q")  # 促音


class Syllable(BaseModel):
    """音節"""

    onset: list[str] = []  # 音節頭
    syllabic: list[str] = []  # 音節主音
    coda: list[str] = []  # 末尾子音
