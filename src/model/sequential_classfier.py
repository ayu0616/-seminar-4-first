from typing import Type

import numpy as np

from model.score import CaseScore
from type import CrfFeatures, CrfLabelSequence
from type.features import CrfLabel


class SequentialClassifier:
    def __init__(self, model: Type):
        self.model = model

    def fit(self, X: list[list[CrfFeatures]], y: list[CrfLabelSequence], **kwargs):
        """学習を行う"""
        n = len(X)
        X_: list[list[list[int]]] = CrfFeatures.get_numbered_features(X)
        for i in range(n):
            m = len(X_[i])
            total_mora_len = 0
            for j in range(m):
                if j > 0:
                    label = y[i][j - 1]
                    idx = CrfFeatures.to_int_idx[label]
                    X_[i][j][idx] = 1
                tml_idx = CrfFeatures.to_int_idx["total_mora_len"]
                X_[i][j][tml_idx] = total_mora_len
                if CrfLabel.is_abbr(y[i][j]):
                    total_mora_len += 1
        flatten_X = sum(X_, [])
        flatten_y = sum(y, CrfLabelSequence())
        self.model.fit(flatten_X, flatten_y, **kwargs)

    def predict(self, X: list[list[CrfFeatures]]) -> list[CrfLabelSequence]:
        """予測を行う"""
        n = len(X)
        res: list[CrfLabelSequence] = []
        X_: list[list[list[int]]] = CrfFeatures.get_numbered_features(X)
        for i in range(n):
            x = X_[i]
            m = len(x)
            y_pred: CrfLabelSequence = CrfLabelSequence([])
            total_mora_len = 0
            for j in range(m):
                if j > 0:
                    label = y_pred[j - 1]
                    idx = CrfFeatures.to_int_idx[label]
                    x[j][idx] = 1
                tml_idx = CrfFeatures.to_int_idx["total_mora_len"]
                x[j][tml_idx] = total_mora_len
                yj = self.model.predict([x[j]])[0]
                y_pred.append(yj)
                if CrfLabel.is_abbr(yj):
                    total_mora_len += 1
            res.append(y_pred)
        return res

    def score(self, X: list[list[CrfFeatures]], y: list[CrfLabelSequence]):
        """スコアを計算する"""
        y_pred = self.predict(X)
        return [CaseScore.from_test_pred(y_, y_pred_) for y_, y_pred_ in zip(y, y_pred)]

    def predict_proba(self, X: list[list[CrfFeatures]]):
        """確率を予測する"""
        n = len(X)
        class_list: list[str] = self.model.classes_
        X_: list[list[list[int]]] = CrfFeatures.get_numbered_features(X)
        for i in range(n):
            x = X_[i]
            m = len(x)
            y_proba: list[np.ndarray[float]] = []
            total_mora_len = 0
            for j in range(m):
                if j > 0:
                    l_idx = y_proba[j - 1].argmax()
                    label = class_list[l_idx]
                    idx = CrfFeatures.to_int_idx[label]
                    x[j][idx] = 1
                tml_idx = CrfFeatures.to_int_idx["total_mora_len"]
                x[j][tml_idx] = total_mora_len
                yj = self.model.predict_proba([x[j]])[0]
                y_proba.append(yj)
                if CrfLabel.is_abbr(class_list[yj.argmax()]):
                    total_mora_len += 1
            yield y_proba

    def predict_rank(self, X: list[list[CrfFeatures]], rank_n: int):
        """予測確率の上位n位のラベルを返す"""
        n = len(X)
        class_list: list[str] = self.model.classes_
        X_: list[list[list[int]]] = CrfFeatures.get_numbered_features(X)
        for i in range(n):
            x = X_[i]
            m = len(x)
            y_pred_proba: list[float] = [1.0]
            y_pred: list[CrfLabelSequence] = [CrfLabelSequence([])]
            tml_idx = CrfFeatures.to_int_idx["total_mora_len"]
            for j in range(m):
                y_pred_proba_next: list[float] = []
                y_pred_next: list[CrfLabelSequence] = []
                proba_memo: dict[str, np.ndarray[float]] = {}
                for y, p in zip(y_pred, y_pred_proba):
                    label = ""
                    if j > 0:
                        label = y_pred[0][j - 1]
                        idx = CrfFeatures.to_int_idx[label]
                        x[j][idx] = 1
                    tml = sum([1 for y_ in y if CrfLabel.is_abbr(y_)])
                    x[j][tml_idx] = tml
                    # if label not in proba_memo:
                    #     y_proba = self.model.predict_proba([x[j]])[0]
                    #     proba_memo[label] = y_proba
                    # else:
                    #     y_proba = proba_memo[label]
                    y_proba = self.model.predict_proba([x[j]])[0]
                    for k, next_p in enumerate(y_proba):
                        class_name = class_list[k]
                        y_pred_next.append(y + [class_name])
                        y_pred_proba_next.append(p * next_p)
                index_list = np.argsort(y_pred_proba_next)[::-1][:rank_n]
                y_pred = [y_pred_next[i] for i in index_list]
                y_pred_proba = [y_pred_proba_next[i] for i in index_list]
            print(y_pred_proba)
            yield y_pred
