from typing import Type

from score import CaseScore
from type import CrfFeatures, CrfLabelSequence


class SequentialClassifier:
    def __init__(self, model: Type):
        self.model = model

    def fit(self, X: list[list[CrfFeatures]], y: list[CrfLabelSequence], **kwargs):
        """学習を行う"""
        n = len(X)
        X_: list[list[list[int]]] = CrfFeatures.get_numbered_features(X)
        for i in range(n):
            m = len(X_[i])
            for j in range(m):
                if j > 0:
                    label = y[i][j - 1]
                    idx = CrfFeatures.to_int_idx[label]
                    X_[i][j][idx] = 1
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
            for j in range(m):
                if j > 0:
                    label = y_pred[j - 1]
                    idx = CrfFeatures.to_int_idx[label]
                    x[j][idx] = 1
                yj = self.model.predict([x[j]])[0]
                y_pred.append(yj)
            res.append(y_pred)
        return res

    def score(self, X: list[list[CrfFeatures]], y: list[CrfLabelSequence]):
        """スコアを計算する"""
        y_pred = self.predict(X)
        return [CaseScore.from_test_pred(y_, y_pred_) for y_, y_pred_ in zip(y, y_pred)]
