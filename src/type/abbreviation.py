from pydantic import BaseModel

from .element import Element


class AbbreviationBase(BaseModel):
    """略語データの基底クラス

    加工前の論文から取得した略語データ
    """

    abbreviation: str  # 略語
    word: str  # 原語


class Abbreviation(AbbreviationBase):
    """略語データ"""

    abbreviation_element_list: list[Element]  # 略語の要素リスト
    word_element_list: list[Element]  # 原語の要素リスト
