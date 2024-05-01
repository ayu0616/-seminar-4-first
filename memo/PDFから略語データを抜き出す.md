---
tags: 
URL: 
著者: 
created: 2024-05-01 17:12
modified: 2024-05-01 17:20
---

# PDFから略語データを抜き出す

## 作戦

- PDF→HTMLに変換
    - [オンラインでPDFからHTMLに変換](https://www.idrsolutions.com/ja/online-pdf-to-html-converter)
- HTMLから法則性を見出してうまく略語を抽出

## HTML

- 文章の法則
    - `'・'`で始まる
    - 原語
        - `'・'`の次から始まる
        - `'：'`まで続く
        - 略語で省略された部分は小さく表示される
- HTMLの法則
    - 本文は`div.text-container`に入っている
    - `'・'`を含む要素は`elem.getClientRects().x === 130`である
    - 文字
        - 普通の大きさの文字は`span.s1_***`（`***`はページ数）
        - 小さい文字は`span.s2_***`
