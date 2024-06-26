import json

import numpy as np
import optuna
import sklearn_crfsuite
from sklearn.model_selection import KFold
from datetime import datetime

def main():
    from score import CaseScore
    from type.abbreviation import Abbreviation
    from type.features import CrfFeatures, CrfLabelSequence

    def compute_score(model, X_test, y_test):
        y_pred = model.predict(X_test)
        score_list = [CaseScore.from_test_pred(y_, y_pred_) for y_, y_pred_ in zip(y_test, y_pred)]
        return score_list

    # 前処理した略語データを読み込む
    data = list(map(Abbreviation.model_validate, json.load(open("../data/abbreviation.json", "r"))))
    X = [list(map(lambda f: f.get_array(), feature_list)) for feature_list in map(CrfFeatures.from_abbreviation, data)]
    y = list(map(CrfLabelSequence.from_abbreviation, data))

    def objective(trial: optuna.Trial):
        model = sklearn_crfsuite.CRF(
            algorithm="lbfgs",
            all_possible_transitions=True,
            c1=trial.suggest_float("c1", 1e-10, 1e10, log=True),
            c2=trial.suggest_float("c2", 1e-10, 1e10, log=True),
            max_iterations=trial.suggest_int("max_iterations", 1, 100000, log=True),
        )

        kf = KFold(n_splits=5, shuffle=True, random_state=616)
        scores: list[float] = []
        for train_idx, test_idx in kf.split(X):
            X_train = [X[i] for i in train_idx]
            y_train = [y[i] for i in train_idx]
            X_test = [X[i] for i in test_idx]
            y_test = [y[i] for i in test_idx]
            model.fit(X_train, y_train)
            case_score_list = compute_score(model, X_test, y_test)
            score = np.mean([cs.f1 for cs in case_score_list])
            scores.append(score)
        return np.mean(scores)

    study = optuna.create_study(direction="maximize", storage="sqlite:///./optuna.db", study_name=f"crf-{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    study.optimize(objective, n_trials=50)

    print("Number of finished trials:", len(study.trials))
    print("Best trial:", study.best_trial.params)


if __name__ == "__main__":
    import os
    import sys

    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    sys.path.append(os.path.join(cur_dir, ".."))
    main()
