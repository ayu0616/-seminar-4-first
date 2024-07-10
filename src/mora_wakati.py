import re

# 各条件を正規表現で表す
c1 = "[ウクスツヌフムユルグズヅブプヴ][ァィェォ]"  # ウ段＋「ァ/ィ/ェ/ォ」
c2 = "[イキシチニヒミリギジヂビピ][ャュェョ]"  # イ段（「イ」を除く）＋「ャ/ュ/ェ/ョ」
c3 = "[テデ][ィュ]"  # 「テ/デ」＋「ャ/ィ/ュ/ョ」
c4 = "[ァ-ヴー]"  # カタカナ１文字（長音含む）

cond = "(" + c1 + "|" + c2 + "|" + c3 + "|" + c4 + ")"
re_mora = re.compile(cond)


def mora_wakati(kana_text: str):
    return re_mora.findall(kana_text)
