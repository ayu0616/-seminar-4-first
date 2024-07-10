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

<div class="flex-1 overflow-y-auto bg-white border p-4 text-sm">

1. [作りたいモデル](#作りたいモデル)
2. [略語とは](#略語とは)
3. [自然な略語](#自然な略語)
4. [単語について](#単語について)
5. [系列ラベリング](#系列ラベリング)
6. [モデルの概要](#モデルの概要)
7. [複数の候補を推定](#複数の候補を推定)
8. [遊んでみよう](#遊んでみよう)
9. [出力の傾向](#出力の傾向)
10. [出力が偏る理由](#出力が偏る理由)
11. [改善方法](#改善方法)

</div>

## 作りたいモデル

- 入力
    - 外来語
    - カタカナ
    - 要素に分解： `パーソナル` `コンピューター`
- 出力
    - 入力の部分列
    - 略語として適切なものを上位$n$件

## 略語とは

略語とは、
<div class="mx-auto my-6 text-xl">

**元の単語の部分列**

</div>

とここでは定義する。

<br />

単語$W$の部分列は、$2^{|W|}$通り
その中で**人間にとって自然な略語**を推定する
<span class="text-desc">（厳密には、全部削ったものと1つも削らなかったものを除く$2^{|W|}-2$通りが略語としてあり得る）</span>

## 自然な略語

自然な略語は何らかの規則を持つ、と仮定

規則は、**音韻**的なものと**意味**的なものが考えられるがここでは

<div class="mx-auto my-6 text-xl">

**音韻**的なものを用いる

</div>

### 音韻的な規則

- 音の並びの自然さ
- どの位置の音を取るか
    - 先頭か末尾か中間か

## 単語について

- 単語は、**要素**に分解される<span class="text-desc ml-2">（意味による分解）</span>
- 要素は、**モーラ**に分解される<span class="text-desc ml-2">（音による分解）</span>
- モーラは**特徴量**を持つ

<div class="mermaid">
flowchart TD
    A(外来語) --> B1(要素1) & B2(要素2)
    B1 --> C1(モーラ1) & C2(モーラ2) & C3(モーラ3)
</div>

<br>

- ポテトチップス → ポテト・チップス → <span class="p-1 border bg-white rounded">ポ / テ / ト</span>  <span class="p-1 border bg-white rounded">チ / ッ / プ / ス</span>

## 系列ラベリング

- 系列の要素にラベルづけする問題
- 品詞分解や固有表現抽出<span class="text-desc">（人名、日付など）</span>に使われる

<div class="mx-auto my-6 text-xl"

単語を**モーラの系列**として考える→**系列ラベリング**

</div>

- ラベル<span class="text-desc ml-1">（厳密にはもうちょっと複雑）</span>
    - **残る**
    - 残らない
- 例
    - **パ**ー**ソ**ナル**コン**ピューター
    - **スーパー**マーケット

## モデルの概要

- モーラ($x_i$)ごとに、略語に使用するかどうか($y_i$)を判定
- 判定には前回の出力も使用
    - $x_2$と$y_1$を使って$y_2$を推定

<div class="mermaid">
flowchart LR
    subgraph g["Sequential Model"]
        direction LR
        subgraph g1[" "]
            direction TB
            x1((x1)) --> model1(RF) --> y1((y1))
        end
        subgraph g2[" "]
            direction TB
            x2((x2)) --> model2(RF) --> y2((y2))
        end
        subgraph g3[" "]
            direction TB
            x3((x3)) --> model3(RF) --> y3((y3))
        end
    end
    g1 --> g2 --> g3
    style g fill:#ecfdf5
    style g1 fill:#FFF
    style g2 fill:#FFF
    style g3 fill:#FFF
</div>

## 複数の候補を推定

分類タスクを複数回連続で行うため精度が出にくい
→複数の候補を推定する

### 推定方法

`sklearn`の`predict_proba`を用いる
`[0.1, 0.25, 0.35, 0.3]`のように各クラスの確率？が出力される

<br>

$R$個の候補を確率が高い順に取得したい
$i$個目のモーラまで見たとき、候補$C_{ir}=(y_{i1}, \cdots, y_{ir})$の出現確率を$p_{ir}$とすると、
$p_{i+1,r}$は$\{p_{ir} \cdot \text{pred}(y_{ir})_k \mid 1 \le k \le K, \quad 1 \le r \le R\}$の$r$番目に大きな値
$p_{i+1,r}$は$KR$個作ることができるが、$R$個だけ保持しておけば良い

## 遊んでみよう

<div class="flex-1 flex">

<div class="text-sm">

例のごとく、Webアプリをつくりました
遊んでみましょう！

<br>

いろいろ試したが、事故リスク大
→事前に試した中で成功／失敗例を紹介

- 成功例
    - <code class="select-all">コロナ</code>・<code class="select-all">ウイルス</code>
    - <code class="select-all">ガクセイジダイ</code>・<code class="select-all">チカラヲイレタコト</code>
- 失敗例
    - <code class="select-all">インターネット</code>
    - <code class="select-all">ユニバーサル</code>・<code class="select-all">スタジオ</code>・<code class="select-all">ジャパン</code>

</div>

<div class="h-full flex-1 overflow-y-auto">
    <iframe src="https://abbreviation-zhqzb2nbkq-an.a.run.app/" class="size-full">
    </iframe>
</div>

</div>

## 出力の傾向

<div class="mx-auto mt-2 mb-6 text-xl">

**先頭から連続した部分**しか取らないことが多い

</div>

- 最初の要素の先頭の数モーラしか取らない
- 最初の要素の全体を取る

## 出力が偏る理由

### データの偏り

- 外来語略語には前部を残すものが多い

### モデルの特性

- 前の推定結果しか見ていない
- 略語判定されやすい条件<span class="text-desc ml-2">（最初の要素の最初のモーラはすべて満たす）</span>
    - それまでに略語判定されたモーラがない
    - 1つ前のモーラが略語判定された

## 改善方法

いくつか考えられるが、時間がなく、、、

<br>

- 後ろから見る方法も取り入れる
- 学習データの偏りを解消する

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
