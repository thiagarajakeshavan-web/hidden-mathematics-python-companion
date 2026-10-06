"""Synthetic fixtures and transparent metrics for Chapters 10--13 only."""
import numpy as np
from scipy.special import expit
from sklearn import metrics
from sklearn.model_selection import train_test_split

FEATURE_NAMES = ["stock_cover_days", "demand_index", "promotion_flag", "lead_time_days"]

def classification_data(seed, n=800):
    """Independent fictional product-period rows; no real customer/store records.

    All inputs exist before the prediction point. The target is a simulated
    next-period replenishment flag, not a purchase decision or allergen verdict.
    This IID design intentionally does not establish time-series performance.
    """
    rng = np.random.default_rng(seed)
    stock = rng.uniform(1, 14, n)
    demand = np.clip(rng.normal(1, .3, n), .1, None)
    promotion = rng.binomial(1, .3, n)
    lead = rng.integers(1, 8, n)
    x = np.column_stack([stock, demand, promotion, lead])
    logit = 1.1*(7-stock)/3 + 1.3*(demand-1)/.3 + .8*promotion + .3*(lead-4)
    # A stated interaction makes a purely linear log-odds model imperfect.
    logit += .7*promotion*(stock < 5)
    probability = expit(logit)
    y = rng.binomial(1, probability)
    return x, y

def three_way_indices(y, seed, train_fraction=.6, validation_fraction=.2):
    """Stratified disjoint indices with the final test portion reserved first."""
    y = np.asarray(y)
    if train_fraction <= 0 or validation_fraction <= 0 or train_fraction+validation_fraction >= 1:
        raise ValueError("All three split fractions must be positive.")
    indices = np.arange(len(y))
    development, test = train_test_split(indices, test_size=1-train_fraction-validation_fraction,
                                          stratify=y, random_state=seed)
    train, validation = train_test_split(development,
        test_size=validation_fraction/(train_fraction+validation_fraction),
        stratify=y[development], random_state=seed+1)
    return train, validation, test

def binary_metrics(y, probability, threshold=.5):
    """Threshold fixed before test inspection; Brier is not calibration alone."""
    y, probability = np.asarray(y), np.asarray(probability, dtype=float)
    if y.ndim != 1 or set(np.unique(y)) != {0, 1}:
        raise ValueError("Binary metrics require a one-dimensional label array with both classes 0 and 1.")
    if probability.shape != y.shape or not np.isfinite(probability).all():
        raise ValueError("Probabilities must be finite and match the label shape.")
    if np.any((probability < 0) | (probability > 1)) or not 0 <= threshold <= 1:
        raise ValueError("Probabilities and threshold must lie in [0,1].")
    prediction = (probability >= threshold).astype(int)
    return {"n": len(y), "positive_count": int(y.sum()), "threshold": threshold,
            "accuracy": float(metrics.accuracy_score(y, prediction)),
            "balanced_accuracy": float(metrics.balanced_accuracy_score(y, prediction)),
            "roc_auc": float(metrics.roc_auc_score(y, probability)),
            "average_precision": float(metrics.average_precision_score(y, probability)),
            "log_loss_nats": float(metrics.log_loss(y, probability, labels=[0, 1])),
            "brier_score": float(metrics.brier_score_loss(y, probability)),
            "confusion_tn_fp_fn_tp": metrics.confusion_matrix(y, prediction, labels=[0, 1]).ravel().tolist()}

def regression_metrics(y, prediction):
    return {"n": len(y), "mae": float(metrics.mean_absolute_error(y, prediction)),
            "mse": float(metrics.mean_squared_error(y, prediction)),
            "rmse": float(np.sqrt(metrics.mean_squared_error(y, prediction))),
            "r_squared": float(metrics.r2_score(y, prediction))}
