from datetime import datetime

def main():
    import json

    import numpy as np
    import optuna
    from sklearn.model_selection import KFold
    from sklearn.svm import SVC

    from sequential_classfier import SequentialClassifier
    from type.abbreviation import Abbreviation
    from type.features import CrfFeatures, CrfLabelSequence

    # 前処理した略語データを読み込む
    data = list(map(Abbreviation.model_validate, json.load(open("../data/abbreviation.json", "r"))))
    X = [*map(CrfFeatures.from_abbreviation, data)]
    y = list(map(CrfLabelSequence.from_abbreviation, data))
    # ラベルの番号振り
    CrfFeatures.get_numbered_features(X)

    def objective(trial: optuna.Trial):
        C = trial.suggest_float("C", 1e-10, 1e10, log=True)
        gamma = trial.suggest_float("gamma", 1e-10, 1e10, log=True)
        model = SequentialClassifier(SVC(C=C, gamma=gamma, random_state=616))
        kf = KFold(n_splits=5, shuffle=True, random_state=616)
        scores: list[float] = []
        for train_idx, test_idx in kf.split(X):
            X_train = [X[i] for i in train_idx]
            y_train = [y[i] for i in train_idx]
            X_test = [X[i] for i in test_idx]
            y_test = [y[i] for i in test_idx]
            model.fit(X_train, y_train)
            case_score_list = model.score(X_test, y_test)
            score = np.mean([cs.f1 for cs in case_score_list])
            scores.append(score)
        return np.mean(scores)

    study = optuna.load_study(study_name="svm", storage="sqlite:///./optuna.db")
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
