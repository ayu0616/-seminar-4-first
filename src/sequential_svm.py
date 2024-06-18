from typing import Literal

from sklearn.svm import SVC

from type import CrfFeatures, CrfLabelSequence


class SequentialSVM(SVC):

    def __init__(
        self,
        kernel: Literal["linear", "poly", "rbf", "sigmoid", "precomputed"] = "rbf",
        degree: int = 3,
        gamma: float | Literal["scale", "auto"] = "scale",
        coef0: float = 0,
        shrinking: bool = True,
        probability: bool = False,
        tol: float = 0.001,
        cache_size: float = 200,
        class_weight: str | None = None,
        verbose: bool = False,
        max_iter: int = -1,
        decision_function_shape: Literal["ovo", "ovr"] = "ovr",
        break_ties: bool = False,
        random_state: int | None = None,
    ):
        super().__init__(
            kernel=kernel,
            degree=degree,
            gamma=gamma,
            coef0=coef0,
            shrinking=shrinking,
            probability=probability,
            tol=tol,
            cache_size=cache_size,
            class_weight=class_weight,
            verbose=verbose,
            max_iter=max_iter,
            decision_function_shape=decision_function_shape,
            break_ties=break_ties,
            random_state=random_state,
        )

    def fit(self, X: list[list[CrfFeatures]], y: list[CrfLabelSequence]):
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
        super().fit(flatten_X, flatten_y)

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
                yj = super().predict([x[j]])[0]
                y_pred.append(yj)
            res.append(y_pred)
        return res
