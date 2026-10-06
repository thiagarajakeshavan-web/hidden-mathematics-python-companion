"""V1C08-CASE01: metrics, thresholds, calibration, and leakage evidence."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from common import emit

SEED = 808
Y = np.array([1, 1, 0, 0, 1, 0, 0, 0])
P = np.array([.9, .6, .8, .4, .3, .2, .1, .05])

def threshold_metrics(y, p, threshold, false_positive_cost=2., false_negative_cost=10.):
    predicted = np.asarray(p) >= threshold
    tn, fp, fn, tp = metrics.confusion_matrix(y, predicted, labels=[0, 1]).ravel()
    return {"threshold": threshold, "true_positive": int(tp), "false_positive": int(fp),
            "false_negative": int(fn), "true_negative": int(tn),
            "precision": float(tp/(tp+fp)) if tp+fp else None,
            "recall": float(tp/(tp+fn)) if tp+fn else None,
            "f1": float(2*tp/(2*tp+fp+fn)) if 2*tp+fp+fn else None,
            "accuracy": float(metrics.accuracy_score(y, predicted)),
            "specificity": float(tn / (tn + fp)) if tn + fp else None,
            "total_cost": float(false_positive_cost * fp + false_negative_cost * fn)}

def pairwise_auc(y, probabilities):
    positives = probabilities[y == 1]
    negatives = probabilities[y == 0]
    if len(positives) == 0 or len(negatives) == 0:
        raise ValueError("ROC AUC requires both positive and negative examples.")
    return float(np.mean((positives[:, None] > negatives).astype(float) + 0.5 * (positives[:, None] == negatives)))

def calibration_bins(y, probabilities):
    edges = np.array([0., .2, .4, .6, .8, 1.])
    bins = []
    for i, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
        mask = (probabilities >= lo) & ((probabilities < hi) if i < 4 else (probabilities <= hi))
        if mask.any():
            bins.append({"lower_inclusive": float(lo), "upper": float(hi), "upper_inclusive": i == 4,
                         "count": int(mask.sum()), "mean_probability": float(probabilities[mask].mean()),
                         "observed_fraction_positive": float(y[mask].mean())})
    return bins

def group_leakage_experiment():
    rng = np.random.default_rng(SEED)
    group_count, rows_per_group = 200, 5
    groups = np.repeat(np.arange(group_count), rows_per_group)
    labels = rng.integers(0, 2, group_count)
    fingerprints = rng.normal(size=(group_count, 8))
    x = fingerprints[groups] + rng.normal(0, .001, (len(groups), 8))
    y = labels[groups]
    random_train, random_test = train_test_split(np.arange(len(y)), test_size=.3, random_state=SEED)
    group_train, group_test = next(GroupShuffleSplit(n_splits=1, test_size=.3, random_state=SEED).split(x, y, groups))
    results = {}
    for name, train, test in [("random_row_split", random_train, random_test), ("unseen_group_split", group_train, group_test)]:
        m = KNeighborsClassifier(n_neighbors=1).fit(x[train], y[train])
        overlap = set(groups[train]) & set(groups[test])
        results[name] = {"train_rows": len(train), "test_rows": len(test), "overlapping_groups": len(overlap),
                         "test_accuracy": float(metrics.accuracy_score(y[test], m.predict(x[test])))}
    return {"seed": SEED, "groups": group_count, "rows_per_group": rows_per_group,
            "deployment_question": "Predict labels for previously unseen entities.",
            "data": "Random entity fingerprint plus tiny noise; random label fixed within entity.",
            "splits": results,
            "interpretation": "For unseen-entity deployment, shared entities in a row split let the model memorize identity. This is not evidence that group splitting is required for every possible deployment question."}

def temporal_leakage_experiment():
    rng = np.random.default_rng(SEED + 1)
    n = 500
    event_time = np.arange(n)
    decision_time = event_time
    legitimate_feature = rng.normal(size=n)
    y = rng.integers(0, 2, n)
    # Deliberate anti-pattern: outcome-derived field arrives one day AFTER prediction.
    leaked_future_feature = y.astype(float)
    feature_available_time = event_time + 1
    train = np.arange(350)
    test = np.arange(350, n)
    safe_model = DecisionTreeClassifier(max_depth=3, random_state=SEED).fit(legitimate_feature[train, None], y[train])
    unsafe_x = np.column_stack([legitimate_feature, leaked_future_feature])
    unsafe_model = DecisionTreeClassifier(max_depth=3, random_state=SEED).fit(unsafe_x[train], y[train])
    return {"seed": SEED + 1, "train_end_time": int(event_time[train].max()), "test_start_time": int(event_time[test].min()),
            "rows_with_future_feature_unavailable_at_decision": int(np.sum(feature_available_time > decision_time)),
            "chronological_safe_accuracy": float(metrics.accuracy_score(y[test], safe_model.predict(legitimate_feature[test, None]))),
            "chronological_leaked_accuracy": float(metrics.accuracy_score(y[test], unsafe_model.predict(unsafe_x[test]))),
            "availability_rule": "A feature must have available_at <= decision_at for that prediction.",
            "interpretation": "Even chronological splitting cannot repair an outcome-derived field unavailable at prediction time. The 100% score is deliberately invalid evidence."}

def run():
    fpr, tpr, thresholds = metrics.roc_curve(Y, P, drop_intermediate=False)
    precision, recall, pr_thresholds = metrics.precision_recall_curve(Y, P)
    true = np.array([10., 20., 30.])
    predicted = np.array([12., 18., 33.])
    return {"chapter": "V1C08", "case_id": "V1C08-CASE01", "synthetic": True,
            "labels": Y, "probabilities": P, "threshold_results": [threshold_metrics(Y, P, t) for t in [.5, .3, .2]],
            "edge_cases": {"no_predicted_positive": threshold_metrics(np.array([0,1]),np.array([.1,.1]),.5),
                           "no_actual_positive": threshold_metrics(np.array([0,0]),np.array([.1,.1]),.5),
                           "undefined_metric_representation": "JSON null; pairwise_auc raises ValueError when either true class is absent."},
            "roc_auc": float(metrics.roc_auc_score(Y, P)), "pairwise_auc_crosscheck": pairwise_auc(Y, P),
            "average_precision": float(metrics.average_precision_score(Y, P)),
            "brier_score": float(metrics.brier_score_loss(Y, P)), "log_loss_nats": float(metrics.log_loss(Y, P)),
            "roc_curve": [{"threshold": None if np.isinf(th) else float(th), "fpr": float(f), "tpr": float(t)} for th, f, t in zip(thresholds, fpr, tpr)],
            "precision_recall_curve": [{"threshold": float(pr_thresholds[i]) if i < len(pr_thresholds) else None,
                                         "precision": float(p), "recall": float(r)} for i, (p, r) in enumerate(zip(precision, recall))],
            "curve_note": "ROC null threshold is +infinity; PR final null threshold is the conventional endpoint. Average precision is not trapezoidal PR area.",
            "calibration_bins": calibration_bins(Y, P),
            "calibration_caveat": "Eight examples illustrate bin arithmetic, not a trustworthy calibration estimate. Intervals are left-closed, right-open except the final bin includes 1.",
            "calibrated_probability_cost_threshold": 2 / (2 + 10),
            "threshold_caveat": "Threshold costs on the same eight rows are retrospective teaching comparisons. Choose operational thresholds on separate validation data with appropriate prevalence, calibration and capacity checks.",
            "imbalance_counts": {"n": 10000, "positive": 100, "tp": 80, "fn": 20, "fp": 198, "tn": 9702,
                                 "accuracy": 9782 / 10000, "precision": 80 / 278, "recall": .8, "f1": 160 / 378, "false_positive_rate": .02},
            "regression": {"y": true, "prediction": predicted, "mae": float(metrics.mean_absolute_error(true, predicted)),
                           "mse": float(metrics.mean_squared_error(true, predicted)), "rmse": float(np.sqrt(metrics.mean_squared_error(true, predicted))),
                           "r_squared": float(metrics.r2_score(true, predicted))},
            "group_leakage": group_leakage_experiment(), "temporal_leakage": temporal_leakage_experiment()}

if __name__ == "__main__":
    emit("V1C08", run())
