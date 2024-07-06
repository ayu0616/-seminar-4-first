---
marp: true
size: 16:9
lang: ja
math: katex
title: 機械学習による外来語略語の推定
transition: fade
---

<!-- transition: fade 300ms -->

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
    - 要素に分解： `パーソナル` `コンピューター`
- 出力
    - 入力の部分列
    - 略語として適切なものを上位$n$件

## 略語とは

- コンピューターで扱いやすい定義にしたい
    - 表記が変わると面倒（カタカナ→Alphabet）

<br>

略語とは、
<div class="mx-auto my-1 text-xl">

**元の単語の部分列**

</div>

とここでは定義する。

<br />

単語$W$の部分列は、$2^{|W|}$通り<span class="text-desc mx-2">（厳密には、全部削ったものと1つも削らなかったものを除く$2^{|W|}-2$通り）</span>
その中で**人間にとって自然な略語**を推定する

## 自然な略語

自然な略語は何らかの規則を持つ、と仮定

規則は、**音韻**的なものと**意味**的なものが考えられるがここでは

<div class="mx-auto my-1 text-xl">

**音韻**的なものを用いる

</div>

### 音韻的な規則

- 音の並びの自然さ
    - 言語学で言うところの音素配列論
- どの位置の音を取るか
    - 先頭か末尾か中間か

## モデルの概要

<link rel="stylesheet" href="./dist/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com/"></script>
<script src="./tailwind.config.js"></script>
