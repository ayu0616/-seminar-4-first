from pydantic import BaseModel


class Mora(BaseModel):
    """モーラ"""

    vowel: str  # 母音
    consonant: str  # 子音


SYLLABIC_NASAL = Mora(vowel="", consonant="N")  # 撥音
SOKUON = Mora(vowel="", consonant="Q")  # 促音


