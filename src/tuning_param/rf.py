import json
from datetime import datetime

import numpy as np
import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold


def main():
    from model.sequential_classfier import SequentialClassifier
    from type.abbreviation import Abbreviation
    from type.features import CrfFeatures, CrfLabelSequence

    # 前処理した略語データを読み込む
    data = list(map(Abbreviation.model_validate, json.load(open("../data/abbreviation.json", "r"))))
    X = [*map(CrfFeatures.from_abbreviation, data)]
    y = list(map(CrfLabelSequence.from_abbreviation, data))
    # ラベルの番号振り
    CrfFeatures.to_int_idx = {}
    CrfFeatures.assign_feature_idx(X)

    def objective(trial: optuna.Trial):
        model = SequentialClassifier(
            RandomForestClassifier(
                random_state=616,
                n_jobs=-1,
                criterion="gini",
                n_estimators=trial.suggest_int("n_estimators", 1, 1000),
                max_depth=trial.suggest_int("max_depth", 1, 500),
                max_features=trial.suggest_float("max_features", 0, 1.0),
                max_leaf_nodes=trial.suggest_int("max_leaf_nodes", 1, 1000),
                min_samples_split=trial.suggest_int("min_samples_split", 2, 5),
                min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 4),
            )
        )
        kf = KFold(n_splits=5, shuffle=True, random_state=616)
        scores: list[float] = []
        for train_idx, test_idx in kf.split(X):
            X_train = [X[i] for i in train_idx]
            y_train = [y[i] for i in train_idx]
            X_test = [X[i] for i in test_idx]
            y_test = [y[i] for i in test_idx]
            model.fit(X_train, y_train)
            case_score_list = model.score(X_test, y_test)
            score = np.mean(case_score_list)
            scores.append(score)
        return np.mean(scores)

    study = optuna.load_study(study_name="rf1", storage="sqlite:///./optuna.db")
    study.optimize(objective, n_trials=100)

    print("Number of finished trials:", len(study.trials))
    print("Best trial:", study.best_trial.params)


if __name__ == "__main__":
    import os
    import sys

    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    sys.path.append(os.path.join(cur_dir, ".."))
    main()
