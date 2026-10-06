"""Quantization, pruning, categorical distillation and analytic memory accounting."""
import numpy as np
from .numerics import array, probabilities, positive, softmax, log_softmax, central_gradient


def quantize(weights, qmax=127):
    w = array(weights, name="weights")
    if not isinstance(qmax, int) or not 1 <= qmax <= 127:
        raise ValueError("int8 qmax must be an integer in [1,127]")
    largest = float(np.max(np.abs(w)))
    scale = largest/qmax if largest else 1.0
    if scale == 0:
        raise ValueError("quantization scale is not representable in float64")
    integers = np.clip(np.rint(w/scale), -qmax, qmax).astype(np.int8)
    reconstructed = integers.astype(np.float64)*scale
    return {"scale": scale, "integers": integers, "reconstructed": reconstructed,
            "max_absolute_error": float(np.max(np.abs(reconstructed-w))),
            "mean_squared_error": float(np.mean((reconstructed-w)**2))}


def prune(weights, threshold):
    w = array(weights)
    threshold = positive(threshold, "pruning threshold", allow_zero=True)
    result = np.where(np.abs(w) < threshold, 0.0, w)
    return {"pruned": result, "pruning_keep_mask": np.abs(w) >= threshold, "sparsity": float(np.mean(result == 0))}


def kl_divergence(teacher, student):
    t, s = probabilities(teacher), probabilities(student)
    if t.shape != s.shape or np.any((t > 0) & (s <= 0)):
        raise ValueError("matching distributions and positive student mass on teacher support required")
    nonzero = t > 0
    return float(np.sum(t[nonzero]*(np.log(t[nonzero])-np.log(s[nonzero]))))


def distill(teacher, student, steps=20, learning_rate=0.5):
    t, s = probabilities(teacher), probabilities(student)
    if t.shape != s.shape or np.any(s <= 0) or not isinstance(steps, int) or steps < 0:
        raise ValueError("matching distributions, positive student and nonnegative steps required")
    eta = positive(learning_rate, "learning rate")
    logits = np.log(s)
    def objective(z):
        nonzero = t > 0
        return float(np.sum(t[nonzero]*(np.log(t[nonzero])-log_softmax(z)[nonzero])))
    initial_gradient = softmax(logits)-t
    finite_difference = central_gradient(objective, logits)
    losses = [objective(logits)]
    for _ in range(steps):
        p = softmax(logits)
        logits -= eta*(p-t)
        losses.append(objective(logits))
    return {"steps": steps, "learning_rate": eta, "kl_before": losses[0],
            "kl_after": losses[-1], "student_after": softmax(logits), "kl_trajectory": losses,
            "gradient_check": {"analytic": initial_gradient, "central_difference": finite_difference,
                               "max_gradient_error": float(np.max(np.abs(initial_gradient-finite_difference)))}}


def integer_count(value, name):
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def run(i):
    if i["rounding"] != "nearest ties to even":
        raise ValueError("only nearest ties-to-even rounding is implemented")
    n = integer_count(i["parameter_count"], "parameters")
    scale_bytes = integer_count(i["scale_bytes"], "scale bytes")
    kv = i["kv"]
    kv_bytes = 2
    for name in ("layers", "batch", "sequence", "kv_heads", "head_dimension", "bytes_per_element"):
        kv_bytes *= integer_count(kv[name], name)
    return {**quantize(i["weights"], i["qmax"]), **prune(i["pruning_weights"], i["pruning_threshold"]),
            "kl_teacher_student_nats": kl_divergence(i["teacher"], i["student"]),
            "categorical_student_training": distill(i["teacher"], i["student"]),
            "dense_fp32_bytes": n*4, "int8_tensor_bytes_with_scale": n+scale_bytes,
            "weight_storage_ratio": n*4/(n+scale_bytes), "kv_bytes": kv_bytes, "kv_mib": kv_bytes/(1024**2)}
