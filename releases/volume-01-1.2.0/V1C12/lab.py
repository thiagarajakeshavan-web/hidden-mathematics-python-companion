"""V1C12-CASE01: exact split gains and a leakage-safe ensemble comparison."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from classical_common import classification_data, three_way_indices, binary_metrics, FEATURE_NAMES
from common import emit

SEED = 1212

def binary_impurity(positive, total, criterion="gini"):
    if total <= 0 or not 0 <= positive <= total or criterion not in ("gini", "entropy"):
        raise ValueError("Use positive total, valid positive count, and gini or entropy.")
    p = positive / total
    if criterion == "gini":
        return 2*p*(1-p)
    return -sum(q*np.log2(q) for q in (p, 1-p) if q > 0)

def split_gain(left_positive, left_total, right_positive, right_total, criterion="gini"):
    left = binary_impurity(left_positive, left_total, criterion)
    right = binary_impurity(right_positive, right_total, criterion)
    total = left_total+right_total
    parent = binary_impurity(left_positive+right_positive, total, criterion)
    weighted = (left_total*left + right_total*right)/total
    return {"parent": parent, "left": left, "right": right, "weighted_children": weighted, "gain": parent-weighted}

def split_fixture():
    x = np.array([0.] * 4 + [1.] * 8).reshape(-1, 1)
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0])
    stump = DecisionTreeClassifier(max_depth=1, random_state=SEED).fit(x, y)
    return {"x": x.ravel(), "y": y, "left_total": 4, "left_positive": 0,
            "right_total": 8, "right_positive": 6,
            "gini": split_gain(0, 4, 6, 8), "entropy_bits": split_gain(0, 4, 6, 8, "entropy"),
            "fitted_stump_threshold": stump.tree_.threshold[0],
            "pruning_alpha_tie": .25, "root_cost_at_tie": .5+.25, "stump_cost_at_tie": .25+2*.25,
            "fitted_stump_probabilities": stump.predict_proba([[0], [1]])[:, 1]}

def boosting_fixture():
    x = np.arange(4., dtype=float).reshape(-1, 1)
    y = np.array([2., 4., 8., 10.])
    f0 = float(y.mean())
    residuals = y-f0
    stump = DecisionTreeRegressor(max_depth=1, random_state=SEED).fit(x, residuals)
    update = stump.predict(x)
    eta = .5
    prediction = f0+eta*update
    full_step = f0+update
    return {"case_id": "V1C12-CASE02", "x": x.ravel(), "y": y, "initial_prediction": f0,
            "residuals": residuals, "stump_threshold": stump.tree_.threshold[0], "stump_prediction": update,
            "learning_rate": eta, "updated_prediction": prediction, "initial_mse": np.mean((y-f0)**2),
            "updated_mse": np.mean((y-prediction)**2), "eta_one_prediction": full_step,
            "eta_one_mse": np.mean((y-full_step)**2),
            "note": "A squared-error regression step. Classification boosting uses a different loss/link; this fixture does not describe a probability update."}

def model_candidates():
    # Parameters are deliberately modest and declared before test inspection.
    return {"logistic_baseline": make_pipeline(StandardScaler(), LogisticRegression(C=1., max_iter=2000)),
            "decision_tree": DecisionTreeClassifier(max_depth=4, min_samples_leaf=12, random_state=SEED),
            "random_forest": RandomForestClassifier(n_estimators=80, max_depth=5, min_samples_leaf=6,
                                                     max_features="sqrt", random_state=SEED, n_jobs=1),
            "gradient_boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=.05, max_depth=2,
                                                            min_samples_leaf=8, random_state=SEED)}

def comparison():
    x, y = classification_data(SEED, 800)
    train, validation, test = three_way_indices(y, SEED)
    validation_scores = {}
    candidates = model_candidates()
    for name, model in candidates.items():
        model.fit(x[train], y[train])
        validation_scores[name] = binary_metrics(y[validation], model.predict_proba(x[validation])[:, 1])
    selected = min(validation_scores, key=lambda name: validation_scores[name]["log_loss_nats"])
    development = np.concatenate([train, validation])
    test_scores = {}
    # After selection, refit each prespecified family on the same development rows.
    for name, model in {"prior_baseline": DummyClassifier(strategy="prior"), **candidates}.items():
        final_model = clone(model).fit(x[development], y[development])
        test_scores[name] = binary_metrics(y[test], final_model.predict_proba(x[test])[:, 1])
    return {"case_id": "V1C12-CASE03", "seed": SEED, "n": len(y), "feature_names": FEATURE_NAMES,
            "target": "synthetic next-period replenishment flag",
            "split_sizes": {"train": len(train), "validation": len(validation), "test": len(test)},
            "split_indices": {"train": train, "validation": validation, "test": test},
            "validation_scores": validation_scores, "selection_metric": "validation log loss (lower is better)",
            "selected_before_test": selected, "refit_rows": len(development), "test_scores": test_scores,
            "note": "All fixed families share rows and features. Test comparison does not revise the validation-selected family. One IID synthetic split gives no production ranking or causal explanation."}

def run():
    return {"case_id": "V1C12-CASE01", "data_status": "constructed and seeded synthetic data",
            "split_fixture": split_fixture(), "boosting_fixture": boosting_fixture(),
            "ensemble_comparison": comparison()}

if __name__ == "__main__":
    emit("V1C12", run())
