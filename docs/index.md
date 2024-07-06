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

- 単語は、**要素**に分解される
- 要素は、**モーラ**に分解される

<div class="mermaid">
flowchart TD
    A(外来語) --> B1(要素1) & B2(要素2)
    B1 --> C1(モーラ1) & C2(モーラ2) & C3(モーラ3)
</div>

<br>

- ポテトチップス → ポテト・チップス → ポ / テ / ト ・ チ / ッ / プ / ス

## モデルの概要

- モーラごとに、略語に使用するかどうかを判定
- 判定には前回の出力も使用

<div class="mermaid">
flowchart LR
    subgraph g1[" "]
        direction TB
        x1((x1)) --> model1(model) --> y1((y1))
    end
    subgraph g2[" "]
        direction TB
        x2((x2)) --> model2(model) --> y2((y2))
    end
    subgraph g3[" "]
        direction TB
        x3((x3)) --> model3(model) --> y3((y3))
    end
    g1 --> g2 --> g3
    style g1 fill:#FFF
    style g2 fill:#FFF
    style g3 fill:#FFF
</div>

<link rel="stylesheet" href="./dist/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com/"></script>
<script src="./tailwind.config.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.0.0/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: true, theme: 'forest' });
window.addEventListener('vscode.markdown.updateContent', function() { mermaid.init() });
</script>
