"""Evaluation on synthetic labels, with paired uncertainty and explicit denominators."""
import math
import numpy as np
from .numerics import array


def binary(values, name="labels"):
    a = array(values, 1, name)
    if np.any((a != 0) & (a != 1)):
        raise ValueError(f"{name} must be binary")
    return a.astype(int)


def confusion(actual, predicted):
    actual, predicted = binary(actual), binary(predicted)
    if actual.shape != predicted.shape:
        raise ValueError("label arrays must match")
    tp = int(np.sum((actual == 1) & (predicted == 1)))
    fp = int(np.sum((actual == 0) & (predicted == 1)))
    fn = int(np.sum((actual == 1) & (predicted == 0)))
    tn = int(np.sum((actual == 0) & (predicted == 0)))
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": tp/(tp+fp) if tp+fp else None,
            "recall": tp/(tp+fn) if tp+fn else None}


def wilson(successes, n, z=1.959963984540054):
    if not isinstance(n, int) or n <= 0 or not isinstance(successes, int) or not 0 <= successes <= n or not math.isfinite(z) or z <= 0:
        raise ValueError("Wilson interval requires integer 0 <= successes <= n, n > 0 and z > 0")
    p, z2 = successes/n, z*z
    center = (p+z2/(2*n))/(1+z2/n)
    half = z*math.sqrt(p*(1-p)/n+z2/(4*n*n))/(1+z2/n)
    return [max(0.0, center-half), min(1.0, center+half)]


def calibration(confidence, correct):
    p, y = array(confidence, 1), binary(correct)
    if p.shape != y.shape or np.any((p < 0) | (p > 1)):
        raise ValueError("matching probabilities and binary outcomes required")
    return {"brier": float(np.mean((p-y)**2)),
            "ece_one_bin": float(abs(np.mean(p)-np.mean(y))),
            "one_bin_membership": list(range(len(p))),
            "one_bin_count": len(p), "one_bin_mean_confidence": float(np.mean(p)),
            "one_bin_accuracy": float(np.mean(y))}


def paired_bootstrap(baseline, candidate, seed, replicates):
    a, b = binary(baseline), binary(candidate)
    if a.shape != b.shape or not isinstance(replicates, int) or not 1 <= replicates <= 100000:
        raise ValueError("paired equal-length labels and 1..100000 replicates required")
    rng = np.random.Generator(np.random.PCG64(seed))
    delta = b-a
    indices = rng.integers(0, len(delta), size=(replicates, len(delta)))
    draws = delta[indices].mean(axis=1)
    return {"paired_improvement": float(delta.mean()),
            "paired_bootstrap_95_percentile_interval": np.quantile(draws, [.025, .975], method="linear"),
            "bootstrap_replicates": replicates, "bootstrap_seed": seed,
            "bootstrap_rng": "NumPy PCG64", "quantile_method": "linear"}


def run(i):
    supported = binary(i["supported"])
    relevant = binary(i["retrieved_relevance"])
    total_relevant = i["total_relevant"]
    if not isinstance(total_relevant, int) or total_relevant < int(relevant.sum()) or total_relevant <= 0:
        raise ValueError("total relevant must be a positive integer at least equal to relevant retrieved")
    return {"faithfulness": float(supported.mean()),
            "faithfulness_wilson_95": wilson(int(supported.sum()), len(supported)),
            "unsupported_detector": confusion(1-supported, i["flagged_unsupported"]),
            **calibration(i["confidence"], i["correct"]),
            "retrieval_precision": float(relevant.mean()), "retrieval_recall": float(relevant.sum()/total_relevant),
            **paired_bootstrap(i["baseline_success"], i["candidate_success"], i["bootstrap_seed"], i["bootstrap_replicates"])}
