"""V1C10-CASE01: regression, logistic arithmetic and held-out experiments."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.special import expit
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from classical_common import classification_data, binary_metrics, regression_metrics, FEATURE_NAMES
from common import emit

SEED = 1010
X_TRAIN = np.array([1., 2., 3., 4.]); Y_TRAIN = np.array([2., 3., 5., 4.])

def regression_fixture():
    x, y = X_TRAIN, Y_TRAIN
    xc, yc = x-x.mean(), y-y.mean()
    sxx, sxy = float(xc@xc), float(xc@yc)
    slope = sxy/sxx; intercept = float(y.mean()-slope*x.mean())
    prediction = intercept+slope*x
    x_test = np.array([5., 6.]); y_test = np.array([5., 7.])
    heldout = intercept+slope*x_test
    ridge = Ridge(alpha=5.).fit(x.reshape(-1, 1), y)
    db = float(np.mean(-y)); dw = float(np.mean(-y*x)); rate=.1
    new_b, new_w = -rate*db, -rate*dw
    return {"x_train_km": x, "y_train_minutes": y, "sxx": sxx, "sxy": sxy,
            "slope": slope, "intercept": intercept, "training_prediction": prediction,
            "training_sse": np.sum((y-prediction)**2), "training_mse": np.mean((y-prediction)**2),
            "x_test_km": x_test, "y_test_minutes": y_test, "test_prediction": heldout,
            "test_metrics": regression_metrics(y_test, heldout), "baseline_train_mean": y.mean(),
            "baseline_test_metrics": regression_metrics(y_test, np.full(len(y_test), y.mean())),
            "gradient": {"loss_definition": "SSE/(2n)", "initial_intercept": 0., "initial_slope": 0.,
                "db": db, "dw": dw, "learning_rate": rate, "updated_intercept": new_b, "updated_slope": new_w,
                "initial_loss": np.mean(y**2)/2, "updated_loss": np.mean((new_b+new_w*x-y)**2)/2},
            "ridge": {"objective": "SSE+lambda*w^2; intercept unpenalized", "lambda": 5.,
                "slope": ridge.coef_[0], "intercept": ridge.intercept_},
            "note": "Tiny constructed travel-time arithmetic; no actual courier data or deployment accuracy claim."}

def logistic_fixture():
    x = np.array([1., 2.5, 4.]); y = np.array([0, 1, 1])
    logits = -2+.8*x; probabilities=expit(logits)
    gradient_b = probabilities[-1]-y[-1]
    return {"coefficients_status": "supplied illustrative coefficients, not fitted estimates",
            "intercept": -2., "slope": .8, "x": x, "y": y, "logits": logits, "probabilities": probabilities,
            "log_loss_nats": log_loss(y, probabilities), "odds_ratio_per_unit": np.exp(.8),
            "at_x4_y1_db": gradient_b, "at_x4_y1_dw": 4*gradient_b}

def regression_data(seed=SEED, n=400):
    rng = np.random.default_rng(seed)
    distance = rng.uniform(.5, 20., n)
    traffic = rng.uniform(0., 1., n)
    pickup_count = rng.integers(1, 5, n)
    x = np.column_stack([distance, traffic, pickup_count])
    y = 4+1.5*distance+8*traffic+.4*pickup_count+rng.normal(0, 2., n)
    return x, y

def heldout_regression():
    x, y = regression_data()
    train, test = train_test_split(np.arange(len(y)), test_size=.25, random_state=SEED)
    fitted = make_pipeline(StandardScaler(), LinearRegression()).fit(x[train], y[train])
    baseline = DummyRegressor(strategy="mean").fit(x[train], y[train])
    scaler = fitted.named_steps["standardscaler"]
    return {"seed": SEED, "feature_names": ["distance_km", "traffic_index", "pickup_count"],
            "generator": "minutes=4+1.5*distance+8*traffic+0.4*pickup_count+Normal(0,2^2)",
            "split_sizes": {"train": len(train), "test": len(test)}, "split_indices": {"train": train, "test": test},
            "training_scaler_mean": scaler.mean_, "scaler_n_samples_seen": int(scaler.n_samples_seen_),
            "baseline_training_mean": baseline.constant_.ravel()[0],
            "test_linear_regression": regression_metrics(y[test], fitted.predict(x[test])),
            "test_training_mean_baseline": regression_metrics(y[test], baseline.predict(x[test])),
            "note": "The linear generator deliberately matches this model. One IID split does not establish robustness to future traffic changes or correlated routes."}

def heldout_classification():
    x, y = classification_data(SEED+1, 800)
    train, test = train_test_split(np.arange(len(y)), test_size=.25, stratify=y, random_state=SEED+1)
    fitted = make_pipeline(StandardScaler(), LogisticRegression(C=1., max_iter=2000)).fit(x[train], y[train])
    baseline = DummyClassifier(strategy="prior").fit(x[train], y[train])
    scaler = fitted.named_steps["standardscaler"]
    return {"seed": SEED+1, "feature_names": FEATURE_NAMES, "target": "synthetic next-period replenishment flag",
            "split_sizes": {"train": len(train), "test": len(test)}, "split_indices": {"train": train, "test": test},
            "training_scaler_mean": scaler.mean_, "scaler_n_samples_seen": int(scaler.n_samples_seen_),
            "baseline_training_prevalence": y[train].mean(),
            "test_logistic_regression": binary_metrics(y[test], fitted.predict_proba(x[test])[:, 1]),
            "test_prior_baseline": binary_metrics(y[test], baseline.predict_proba(x[test])[:, 1]),
            "note": "C=1 and threshold=.5 are fixed in advance. Fitted probabilities are not guaranteed calibrated; report Brier/log loss as proper scores, not proof of calibration. No test-based tuning."}

def run():
    return {"case_id": "V1C10-CASE01", "data_status": "constructed and seeded synthetic data",
            "regression_fixture": regression_fixture(), "logistic_fixture": logistic_fixture(),
            "heldout_regression": heldout_regression(), "heldout_classification": heldout_classification()}

if __name__ == "__main__":
    emit("V1C10", run())
