from pydantic import BaseModel


class Mora(BaseModel):
    """モーラ"""

    vowel: str  # 母音
    consonant: str  # 子音


SYLLABIC_NASAL = Mora(vowel="", consonant="N")  # 撥音
SOKUON = Mora(vowel="", consonant="Q")  # 促音


class SYLLABLE(BaseModel):
    """音節"""

    onset: list[Mora]  # 音節頭
    syllabic: list[Mora]  # 音節主音
    coda: list[Mora]  # 末尾子音

    @property
    def mora_list(self) -> list[Mora]:
        return self.onset + self.syllabic + self.coda
