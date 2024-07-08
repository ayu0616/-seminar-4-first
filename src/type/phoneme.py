from pydantic import BaseModel


class Mora(BaseModel):
    """モーラ"""

    vowel: str  # 母音
    consonant: str  # 子音
