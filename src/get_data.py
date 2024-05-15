"""論文の付録から略語データを入手するためのプログラム"""

import glob
import json
import os
import re

from bs4 import BeautifulSoup

from type import AbbreviationBase

os.chdir(os.path.dirname(os.path.abspath(__file__)))

START = "・"  # 略語部分の開始文字
END = "："  # 略語部分の終了文字


def get_data(html_path: str) -> list[AbbreviationBase]:
    """HTMLファイルごとに略語と原語を取得する関数"""
    with open(html_path, "r") as f:
        soup = BeautifulSoup(f, "html.parser")
    normal_size_class = ""
    small_size_class = ""
    for style in soup.select("style"):
        for line in style.text.split("\n"):
            normal_match = re.match(r"\.(s\d+_\d+){font-size:16px;font-family:MS-Mincho_10-b;color:#000;}", line)
            if normal_match:
                normal_size_class = normal_match.group(1)
            small_match = re.match(r"\.(s\d+_\d+){font-size:10px;font-family:MS-Mincho_10-b;color:#000;}", line)
            if small_match:
                small_size_class = small_match.group(1)
    data: list[AbbreviationBase] = []
    span_list = soup.select("span")
    is_inside = False  # 略語部分に入っているかどうか
    for span in span_list:
        class_list = span.get("class")
        if isinstance(class_list, str):
            class_list = [class_list]
        if not class_list or len(class_list) == 0:
            # クラスがないspanは無視
            continue
        is_normal = len([c for c in class_list if normal_size_class == c]) > 0  # 通常の文字サイズかどうか
        is_small = len([c for c in class_list if small_size_class == c]) > 0  # 小さな文字サイズかどうか
        assert not (is_normal and is_small), "文字サイズが通常と小さな文字の両方になっています"
        text = span.text
        if is_inside:
            if is_normal:
                end_idx = text.find(END)  # 終了文字を探す
                if end_idx != -1:
                    # 終了文字が見つかった場合は略語部分が終わる
                    data[-1].word += text[:end_idx]
                    data[-1].abbreviation += text[:end_idx]
                    is_inside = False
                else:
                    data[-1].word += text
                    data[-1].abbreviation += text
            elif is_small:
                # 小さいサイズは原語のみに含まれる
                data[-1].word += text
        else:
            if text.startswith(START):
                # 開始文字が見つかった場合は略語部分が始まる
                data.append(AbbreviationBase(abbreviation=text[1:], word=text[1:]))
                is_inside = True
        if len(data) and "。" in data[-1].word:
            # "。"が含まれている場合、略語を誤判定しているため、略語部分を脱出してデータを削除
            is_inside = False
            data.pop()
    not_change = [d for d in data if d.abbreviation == d.word]  # 略語と原語が一致しているデータ
    if len(not_change):
        # そのようなデータが存在することはありえないので、警告を出す
        print(f"略語と原語が一致しているデータがあります: {html_path}")
        for d in not_change:
            print(f"略語: {d.abbreviation}, 原語: {d.word}")
    return data


html_path_list: list[str] = glob.glob("../paper-abbreviation/*.html")  # 対象のHTMLファイルのリスト
html_path_list = sorted(html_path_list)
data: list[AbbreviationBase] = []  # 略語データ
for p in html_path_list:
    data += get_data(p)

json.dump([d.model_dump() for d in data], open("./data/abbreviation-base.json", "w"), ensure_ascii=False, indent=4)
