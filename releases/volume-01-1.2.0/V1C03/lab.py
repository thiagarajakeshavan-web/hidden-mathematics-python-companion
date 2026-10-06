"""V1C03-CASE01: conditional probability, base rates and expectation."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.stats import binom, norm, poisson, expon
from common import emit

SEED = 303

def posterior(prevalence, sensitivity=0.9, false_positive_rate=0.05):
    if not all(0 <= p <= 1 for p in [prevalence, sensitivity, false_positive_rate]):
        raise ValueError("Probabilities must lie in [0,1].")
    denominator = sensitivity * prevalence + false_positive_rate * (1 - prevalence)
    if denominator == 0:
        raise ValueError("Conditioning event has zero probability.")
    return sensitivity * prevalence / denominator

def moments(values, probabilities):
    values, p = np.asarray(values, dtype=float), np.asarray(probabilities, dtype=float)
    if values.shape != p.shape or np.any(p < 0) or not np.isclose(p.sum(), 1):
        raise ValueError("Invalid discrete distribution.")
    mean = float(values @ p)
    variance = float(((values - mean) ** 2) @ p)
    return mean, variance

def run():
    mean, variance = moments([0, 1, 2], [0.2, 0.5, 0.3])
    rng = np.random.default_rng(SEED)
    n = 100000
    event = rng.random(n) < 0.01
    positive = rng.random(n) < np.where(event, 0.9, 0.05)
    return {"chapter": "V1C03", "case_id": "V1C03-CASE01", "synthetic": True,
            "bayes": {"prevalence": 0.01, "sensitivity": 0.9, "false_positive_rate": 0.05,
                      "positive_probability": 0.0585, "posterior_event_given_positive": posterior(0.01),
                      "constructed_counts_per_100000": {"true_positive": 900, "false_positive": 4950, "false_negative": 100, "true_negative": 94050}},
            "base_rate_sweep": [{"prevalence": p, "posterior": posterior(p)} for p in [0.001, 0.01, 0.1]],
            "discrete_demand": {"values": [0, 1, 2], "probabilities": [0.2, 0.5, 0.3], "expectation": mean, "second_moment": 1.7, "variance": variance, "standard_deviation": float(np.sqrt(variance))},
            "distribution_examples": {"binomial_n5_p04_probability_k3": float(binom.pmf(3, 5, .4)),
                                      "poisson_mean3_probability_k2": float(poisson.pmf(2, 3)),
                                      "exponential_rate02_probability_above5": float(expon.sf(5, scale=5)),
                                      "normal_standard_probability_between_minus2_and2": float(norm.cdf(2) - norm.cdf(-2))},
            "beta_binomial_update": {"prior_alpha": 2, "prior_beta": 8, "successes": 7, "trials": 10, "posterior_alpha": 9, "posterior_beta": 11, "posterior_mean": 0.45},
            "dependent_uncorrelated": {"x": [-1, 0, 1], "y_equals_x_squared": [1, 0, 1], "covariance": 0.0, "note": "Y is determined by X, despite zero covariance."},
            "monte_carlo": {"seed": SEED, "n": n, "positive_count": int(positive.sum()),
                            "estimated_posterior": float(event[positive].mean()),
                            "note": "Seeded approximation, not the exact Bayes result and not real operational evidence."}}

if __name__ == "__main__":
    emit("V1C03", run())
