from pydantic import BaseModel

from .phoneme import Mora, Syllable


class Element(BaseModel):
    """単語を分解した要素の基底クラス"""

    text: str  # 文字列
    mora_list: list[Mora]  # モーラ列
    syllable_list: list[Syllable]  # 音節列
