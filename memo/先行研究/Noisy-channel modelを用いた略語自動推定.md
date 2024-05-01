---
created: 2024-04-23 10:04
modified: 2024-05-01 15:19
tags:
  - 自然言語処理
  - 外来語
  - 漢字
  - 複合語
URL: https://lr-www.pi.titech.ac.jp/paper/paper/39.pdf
著者:
  - 村山紀文
  - 奥村学
年: 2006
---

# Noisy-channel modelを用いた略語自動推定

```table-of-contents
minLevel: 2
```

## 概要

文章中から略語を発見するシステムを作る

- 略語の作り方
    - 原語を要素に分割
        - これは人力でやっているらしい（700〜800単語）
    - 要素列から略語候補を出力
        - これは以下のモデルを利用している
    - 候補をWeb検索して絞り込む

候補の出力に、Noisy-channel modelを利用する

## Noisy-channel model

最尤推定のような方法で略語の推定を行っている

原語： $O$
略語： $A$

$$
\begin{align}
A &= \arg\max_{A^*} P(A^* \mid O) \\
&= \arg\max_{A^*} \frac{P(A^*)P(O \mid A^*)}{P(O)} \\
&= \arg\max_{A^*} {P(A^*)P(O \mid A^*)}
\end{align}
$$

$A^*$全体の集合の要素数は$2^{|A|}$ぐらいなので現実的な長さの単語については、すべて列挙して最大値を求めることができる
$|A|$： $A$に含まれるモーラの数

### 変換モデル

$P(O\mid A)$は$A$から$O$が生成される確率

- 略語→原語の変換ステップ
    - Expand： 各略語要素の原語要素への復元
    - Insert： 省略された原語要素の復元

## 参考文献

- [World wide web を知識源としたカタカナ語省略形の自動生成](World%20wide%20web%20を知識源としたカタカナ語省略形の自動生成.md)
