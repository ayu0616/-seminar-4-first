---
created: 2024-04-23 10:04
modified: 2024-04-30 17:54
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
    - 要素列から略語候補を出力
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
