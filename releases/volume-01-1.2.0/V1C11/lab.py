"""V1C11-CASE01: Bayes, distance, margins, and honest probability calibration."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.frozen import FrozenEstimator
from sklearn.naive_bayes import BernoulliNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from classical_common import classification_data, three_way_indices, binary_metrics, FEATURE_NAMES
from common import emit

SEED = 1111

def bernoulli_data():
    # A constructed realization of stated marginal counts, not observed records.
    late = np.column_stack([np.arange(10)<8, np.arange(10)<6]).astype(int)
    on_time = np.column_stack([np.arange(30)<6, np.arange(30)<3]).astype(int)
    return np.vstack([late, on_time]), np.array([1]*10+[0]*30)

def naive_bayes_fixture():
    x, y = bernoulli_data()
    query = [[1, 1]]
    unsmoothed = BernoulliNB(alpha=0., force_alpha=True).fit(x, y)
    smoothed = BernoulliNB(alpha=1.).fit(x, y)
    scores = np.array([.25*.8*.6, .75*.2*.1])
    smooth_scores = np.array([.25*(9/12)*(7/12), .75*(7/32)*(4/32)])
    return {"class_counts": {"late": 10, "on_time": 30}, "query": query[0],
            "priors_late_on_time": [.25, .75], "unsmoothed_scores_late_on_time": scores,
            "late_probability_unsmoothed": scores[0]/scores.sum(),
            "sklearn_late_probability_unsmoothed": unsmoothed.predict_proba(query)[0, 1],
            "feature_smoothing_alpha": 1., "smoothed_scores_late_on_time": smooth_scores,
            "late_probability_smoothed": smooth_scores[0]/smooth_scores.sum(),
            "sklearn_late_probability_smoothed": smoothed.predict_proba(query)[0, 1],
            "smoothed_class_priors_on_time_late": np.exp(smoothed.class_log_prior_),
            "note": "Feature likelihoods are smoothed; empirical class priors are unchanged. The conditional-independence assumption is a model assumption, not established by these counts."}

def knn_fixture():
    query = np.array([2., 100.]); x = np.array([[2., 200.], [4., 100.], [3., 180.]])
    labels = np.array([1, 0, 1]); factors=np.array([1., 100.])
    raw = np.linalg.norm(x-query, axis=1); scaled=np.linalg.norm((x-query)/factors, axis=1)
    return {"query": query, "points": x, "labels": labels, "teaching_scale_factors": factors,
            "raw_distances": raw, "scaled_distances": scaled,
            "nearest_raw_label": labels[np.argmin(raw)], "nearest_scaled_label": labels[np.argmin(scaled)],
            "k3_positive_fraction": labels.mean(),
            "note": "Predefined units illustrate geometry. The larger experiment learns StandardScaler on training rows only."}

def svm_fixture():
    x=np.array([-2., -1., 1., 2.]).reshape(-1, 1); y=np.array([-1, -1, 1, 1])
    fitted=SVC(kernel="linear", C=1.).fit(x, y)
    w=float(fitted.coef_[0, 0]); b=float(fitted.intercept_[0])
    return {"x": x.ravel(), "y": y, "w": w, "b": b, "support_vectors": fitted.support_vectors_.ravel(),
            "functional_margins": y*(x.ravel()*w+b), "margin_width": 2/abs(w),
            "hinge_label": -1, "hinge_score": .2, "hinge_loss": max(0., 1-(-1)*.2),
            "rbf_gamma": .5, "squared_distance": 2., "rbf_value": np.exp(-.5*2),
            "ideal_cost_threshold": 2/(2+8),
            "cost_threshold_assumptions": "calibrated probabilities, FP cost2/FN cost8, zero correct-decision costs and independent decisions without capacity constraints",
            "note": "A signed margin is not a probability. The fixed .2 cost threshold is arithmetic, not a threshold fitted to experiment outcomes."}

def fit_classifiers(x, y, train, calibration):
    base = {"gaussian_nb": GaussianNB(),
            "knn": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15, weights="uniform")),
            "rbf_svm": make_pipeline(StandardScaler(), SVC(C=1., kernel="rbf", gamma="scale"))}
    calibrated = {}
    for name, estimator in base.items():
        estimator.fit(x[train], y[train])
        # FrozenEstimator prevents refitting; only calibrator sees these rows.
        calibrated[name] = CalibratedClassifierCV(FrozenEstimator(estimator), method="sigmoid").fit(x[calibration], y[calibration])
    return base, calibrated

def comparison():
    x,y=classification_data(SEED, 1000)
    train,calibration,test=three_way_indices(y, SEED, train_fraction=.5, validation_fraction=.25)
    base,calibrated=fit_classifiers(x,y,train,calibration)
    probabilities={name: fitted.predict_proba(x[test])[:,1] for name,fitted in calibrated.items()}
    prior=DummyClassifier(strategy="prior").fit(x[train], y[train])
    calibrated_scores={name:binary_metrics(y[test],p) for name,p in probabilities.items()}
    raw_scores={name:binary_metrics(y[test],base[name].predict_proba(x[test])[:,1]) for name in ("gaussian_nb", "knn")}
    scalers={name: {"n_samples_seen": int(base[name].named_steps["standardscaler"].n_samples_seen_),
                    "mean":base[name].named_steps["standardscaler"].mean_} for name in ("knn", "rbf_svm")}
    return {"seed":SEED, "feature_names":FEATURE_NAMES, "target":"synthetic next-period replenishment flag",
            "split_sizes":{"train":len(train),"calibration":len(calibration),"test":len(test)},
            "split_indices":{"train":train,"calibration":calibration,"test":test},
            "base_scalers":scalers, "calibration":"Separate 250-row sigmoid calibration for ALL three fixed classifiers; FrozenEstimator prevents base refit.",
            "test_calibrated_classifiers":calibrated_scores, "test_uncalibrated_probability_models":raw_scores,
            "test_training_prior_baseline":binary_metrics(y[test],prior.predict_proba(x[test])[:,1]),
            "svm_test_decision_score_range": [np.min(base["rbf_svm"].decision_function(x[test])), np.max(base["rbf_svm"].decision_function(x[test]))],
            "svm_test_probability_range":[np.min(probabilities["rbf_svm"]),np.max(probabilities["rbf_svm"])],
            "note":"Fixed hyperparameters and .5 threshold; no test-based tuning. All three classifiers receive the same training/calibration rows. The simple prior baseline uses training labels only. Calibration fitting does not guarantee calibration or lower test log loss. Small one-seed IID results are not a universal model ranking."}

def run():
    return {"case_id":"V1C11-CASE01", "data_status":"constructed and seeded synthetic data",
            "naive_bayes_fixture":naive_bayes_fixture(), "knn_fixture":knn_fixture(),
            "svm_fixture":svm_fixture(), "heldout_comparison":comparison()}

if __name__ == "__main__":
    emit("V1C11",run())
