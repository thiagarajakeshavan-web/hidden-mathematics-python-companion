"""Numerically stable helpers with explicit input validation."""
import math
import numpy as np


def array(value, ndim=None, name="array"):
    a = np.asarray(value, dtype=np.float64)
    if a.size == 0 or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be nonempty and finite")
    if ndim is not None and a.ndim != ndim:
        raise ValueError(f"{name} must have {ndim} dimensions")
    return a


def positive(value, name="value", allow_zero=False):
    value = float(value)
    if not math.isfinite(value) or (value < 0 if allow_zero else value <= 0):
        raise ValueError(f"{name} must be finite and {'nonnegative' if allow_zero else 'positive'}")
    return value


def sigmoid(x):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError("logit must be finite")
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def softplus(x):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError("logit must be finite")
    return max(x, 0.0) + math.log1p(math.exp(-abs(x)))


def softmax(logits, allowed=None):
    a = array(logits, name="logits")
    if a.ndim < 1:
        raise ValueError("softmax needs at least one dimension")
    if allowed is None:
        allowed = np.ones_like(a, dtype=bool)
    allowed = np.asarray(allowed, dtype=bool)
    if allowed.shape != a.shape or not np.all(np.any(allowed, axis=-1)):
        raise ValueError("mask must match logits and allow at least one key in every row")
    masked = np.where(allowed, a, -np.inf)
    exp = np.exp(masked - np.max(masked, axis=-1, keepdims=True))
    return exp / exp.sum(axis=-1, keepdims=True)


def log_softmax(logits):
    a = array(logits, name="logits")
    if a.ndim < 1:
        raise ValueError("log-softmax needs at least one dimension")
    shifted = a - np.max(a, axis=-1, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=-1, keepdims=True))


def probabilities(values, name="probabilities"):
    a = array(values, ndim=1, name=name)
    if np.any(a < 0) or not np.isclose(a.sum(), 1.0, atol=1e-10, rtol=0):
        raise ValueError(f"{name} must be nonnegative and sum to one")
    return a


def central_gradient(fn, theta, epsilon=1e-6):
    theta = array(theta, ndim=1, name="parameters")
    epsilon = positive(epsilon, "epsilon")
    result = np.empty_like(theta)
    for j in range(theta.size):
        plus, minus = theta.copy(), theta.copy()
        plus[j] += epsilon
        minus[j] -= epsilon
        result[j] = (fn(plus) - fn(minus)) / (2 * epsilon)
    return result


def json_ready(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {k: json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    return value
