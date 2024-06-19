"""
モデルの比較を行う
"""

import json
import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from lightgbm import LGBMClassifier
from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn_crfsuite import CRF

from sequential_classfier import SequentialClassifier
from type import Abbreviation, CrfFeatures, CrfLabelSequence, crf_label

os.chdir(os.path.dirname(__file__))

data = list(map(Abbreviation.model_validate, json.load(open("data/abbreviation.json"))))


class CaseScore(BaseModel):
    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0
    true_negative: int = 0

    @property
    def precision(self):
        if self.true_positive + self.false_positive == 0:
            return 0
        return self.true_positive / (self.true_positive + self.false_positive)

    @property
    def recall(self):
        if self.true_positive + self.false_negative == 0:
            return 0
        return self.true_positive / (self.true_positive + self.false_negative)

    @property
    def f1(self):
        if self.precision + self.recall == 0:
            return 0
        return 2 * self.precision * self.recall / (self.precision + self.recall)

    @property
    def accuracy(self):
        return (self.true_positive + self.true_negative) / (self.true_positive + self.false_positive + self.false_negative + self.true_negative)


def crf(
    X_train: list[list["CrfFeatures"]], y_train: list["CrfLabelSequence"], X_test: list[list["CrfFeatures"]], y_test: list["CrfLabelSequence"]
) -> list[CaseScore]:
    X_train_ = [[mora.get_array() for mora in word] for word in X_train]
    X_test_ = [[mora.get_array() for mora in word] for word in X_test]
    crf = CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100000, all_possible_transitions=True)
    crf.fit(X_train_, y_train)
    y_pred = crf.predict(X_test_)
    score_list: list[CaseScore] = []
    for true, pred in zip(y_test, y_pred):
        score = CaseScore()
        for t, p in zip(true, pred):
            if t == p:
                if p == crf_label.NG:
                    score.true_negative += 1
                else:
                    score.true_positive += 1
            else:
                if p == crf_label.NG:
                    score.false_positive += 1
                else:
                    score.false_negative += 1
        score_list.append(score)
    return score_list


def sklearn_model(
    model, X_train: list[list["CrfFeatures"]], y_train: list["CrfLabelSequence"], X_test: list[list["CrfFeatures"]], y_test: list["CrfLabelSequence"]
) -> list[CaseScore]:
    model.fit(X_train, y_train)
    y_pred: list[CrfLabelSequence] = model.predict(X_test)
    score_list: list[CaseScore] = []
    for true, pred in zip(y_test, y_pred):
        score = CaseScore()
        for t, p in zip(true, pred):
            if t == p:
                if p == crf_label.NG:
                    score.true_negative += 1
                else:
                    score.true_positive += 1
            else:
                if p == crf_label.NG:
                    score.false_positive += 1
                else:
                    score.false_negative += 1
        score_list.append(score)
    return score_list


crf_score_list: list[CaseScore] = []
svm_score_list: list[CaseScore] = []
lgbm_score_list: list[CaseScore] = []

for i in range(10):
    data_train, data_test = train_test_split(data, test_size=0.2)
    X_train = [*map(CrfFeatures.from_abbreviation, data_train)]
    y_train = list(map(CrfLabelSequence.from_abbreviation, data_train))
    X_test = [*map(CrfFeatures.from_abbreviation, data_test)]
    y_test = list(map(CrfLabelSequence.from_abbreviation, data_test))

    f1 = lambda: crf_score_list.extend(crf(X_train, y_train, X_test, y_test))
    f2 = lambda: svm_score_list.extend(
        sklearn_model(SequentialClassifier(SVC(kernel="rbf", C=1, class_weight="balanced", gamma="auto", probability=True)), X_train, y_train, X_test, y_test)
    )
    f3 = lambda: lgbm_score_list.extend(sklearn_model(SequentialClassifier(LGBMClassifier()), X_train, y_train, X_test, y_test))
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(f1)
        executor.submit(f2)
        executor.submit(f3)

df = pd.DataFrame({"f1": score.f1, "accuracy": score.accuracy, "recall": score.recall, "precision": score.precision} for score in crf_score_list)
print("crf")
print(df.describe())

df = pd.DataFrame({"f1": score.f1, "accuracy": score.accuracy, "recall": score.recall, "precision": score.precision} for score in svm_score_list)
print("svm")
print(df.describe())

df = pd.DataFrame({"f1": score.f1, "accuracy": score.accuracy, "recall": score.recall, "precision": score.precision} for score in lgbm_score_list)
print("lgbm")
print(df.describe())
