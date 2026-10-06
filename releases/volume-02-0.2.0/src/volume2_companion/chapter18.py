"""A supplied BPE merge list, smoothed count language model and synthetic scaling."""
import math
import numpy as np
from .numerics import array, positive, probabilities as distribution


def merge_symbols(symbols, merges):
    if not symbols or any(not isinstance(x, str) or not x for x in symbols):
        raise ValueError("symbols must be nonempty strings")
    ranks = {}
    for j, pair in enumerate(merges):
        if len(pair) != 2 or tuple(pair) in ranks or any(not isinstance(x, str) or not x for x in pair):
            raise ValueError("merge pairs must contain two strings and be unique")
        ranks[tuple(pair)] = j
    current, stages = list(symbols), [list(symbols)]
    while len(current) > 1:
        eligible = [(ranks[(a, b)], (a, b)) for a, b in zip(current, current[1:]) if (a, b) in ranks]
        if not eligible:
            break
        _, selected = min(eligible)
        following, j = [], 0
        while j < len(current):
            if j + 1 < len(current) and tuple(current[j:j+2]) == selected:
                following.append(current[j] + current[j+1]); j += 2
            else:
                following.append(current[j]); j += 1
        current = following
        stages.append(current.copy())
    return stages


def conditional_counts(vocabulary, counts, alpha=1.0):
    n = array(counts, 1, "counts")
    alpha = positive(alpha, "smoothing")
    if len(vocabulary) != len(n) or len(set(vocabulary)) != len(vocabulary) or np.any(n < 0) or np.any(n != np.floor(n)):
        raise ValueError("unique vocabulary and matching nonnegative integer counts required")
    return (n + alpha) / (n.sum() + alpha * len(n))


def negative_log_likelihood(vocabulary, probabilities, targets):
    probabilities = distribution(probabilities)
    if len(probabilities) != len(vocabulary) or len(set(vocabulary)) != len(vocabulary):
        raise ValueError("unique vocabulary must match probabilities")
    if not targets or any(t not in vocabulary for t in targets):
        raise ValueError("evaluation requires known targets")
    selected = np.array([probabilities[vocabulary.index(t)] for t in targets])
    if np.any(selected <= 0):
        raise ValueError("target probabilities must be positive")
    return float(-np.mean(np.log(selected)))


def scaling_fit(observations, floor):
    if not math.isfinite(floor):
        raise ValueError("loss floor must be finite")
    data = array(observations, 2, "scaling observations")
    if data.shape[1] != 2 or len(data) < 2 or np.any(data[:, 0] <= 0) or np.any(data[:, 1] <= floor) or np.unique(data[:, 0]).size < 2:
        raise ValueError("need at least two distinct positive compute values and losses above floor")
    slope, intercept = np.polyfit(np.log(data[:, 0]), np.log(data[:, 1] - floor), 1)
    return float(-slope), float(np.exp(intercept))


def run(i):
    p = conditional_counts(i["next_token_vocabulary"], i["next_token_counts_after_buy"], i["additive_smoothing"])
    nll = negative_log_likelihood(i["next_token_vocabulary"], p, i["evaluation_next_tokens"])
    exponent, coefficient = scaling_fit(i["synthetic_losses"], i["synthetic_loss_floor"])
    return {"merge_stages": merge_symbols(i["initial_symbols"], i["ordered_merges"]),
            "conditional_probabilities": p, "mean_cross_entropy_nats": nll, "perplexity": math.exp(nll),
            "synthetic_power_exponent": exponent,
            "synthetic_prediction_C64": i["synthetic_loss_floor"] + coefficient*64**(-exponent)}
