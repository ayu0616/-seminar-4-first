---
marp: true
size: 16:9
lang: ja
style: |
    section {
        background-color: rgb(248, 250, 252);
        font-family: "BIZ UDPGothic", sans-serif;
        justify-content: start;
        color: #333;
    }
    .area {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;

    }
    h3:first-child, h3:first-child {
        margin-top: 0;
    }
    div.mermaid { all: unset; }
    h1, h2, h3, h4, h5, h6 {
        color: #691f80;
        font-weight: bold;
    }
    section.lead {
        justify-content: center;
    }
    section.lead h1 {
        text-align: center;
    }
    section.narrow {
       padding: 0;
    }
    code {
      font-family: monaco, monospace, "BIZ UDPGothic";
    }
    marp-pre {
      background-color: white;
    }
    ul {
        margin: 0;
    }
    strong {
        color: #691f80;
    }
math: mathjax
title: 機械学習による外来語略語の推定
---

<!-- $width: 1920 -->
<!-- $height: 1080 -->

<!-- headingDivider: 2 -->

<!-- _class: lead -->

# 機械学習による外来語略語の推定

<p class="text-right">経済学部3年 小川歩夢</p>

## もくじ

- [作りたいモデル](#作りたいモデル)

## 作りたいモデル

- 入力
    - 外来語
    - カタカナ
    - 略語は要素に分解： `パーソナル` `コンピューター`
- 出力
    - 入力の部分列
    - 略語として適切なものを上位$n$件

## 略語とは

- コンピューターで扱いやすい定義にしたい
    - 表記が変わると面倒（カタカナ→Alphabet）

<div class="mt-12"></div>

略語とは、
<div class="mx-auto my-1 text-[2.5rem]">

**元の単語の部分列**

</div>
とここでは定義する。

<div class="mt-12"></div>

単語$W$の部分列は、$2^{|W|}$通り
その中で**人間にとって自然な略語**を推定する

## 自然な略語

自然な略語は何らかの共通点を持つ、と仮定

### 共通点

#### 音韻

#### 意味

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com/"></script>
<script src="./tailwind.config.js"></script>
