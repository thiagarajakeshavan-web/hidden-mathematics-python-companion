"""V1C04-CASE01: inference, MLE, and separate LLN/CLT simulations."""
from pathlib import Path
import math
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy import stats
from common import emit

SEED = 404
SAMPLE = np.array([48., 52., 49., 51., 50.])

def mean_inference(sample, null_mean=48.0, confidence=0.95):
    sample = np.asarray(sample, dtype=float)
    n = len(sample)
    if sample.ndim != 1 or n < 2 or not np.all(np.isfinite(sample)) or not 0 < confidence < 1 or sample.std() == 0:
        raise ValueError("Require at least two finite, nonconstant observations and confidence in (0,1).")
    mean = float(sample.mean())
    sd = float(sample.std(ddof=1))
    se = sd / math.sqrt(n)
    critical = float(stats.t.ppf((1 + confidence) / 2, df=n - 1))
    test = stats.ttest_1samp(sample, popmean=null_mean, alternative="two-sided")
    return {"n": n, "mean": mean, "sample_sd_ddof1": sd, "standard_error": se,
            "confidence": confidence, "t_critical": critical,
            "mean_confidence_interval": [mean - critical * se, mean + critical * se],
            "null_mean": null_mean, "t_statistic": float(test.statistic), "two_sided_p_value": float(test.pvalue),
            "degrees_of_freedom": n - 1,
            "assumptions": "Independent random sample from a normal population for exact small-sample t inference; sample is synthetic."}

def bernoulli_log_likelihood(p, successes=7, trials=10):
    if not 0 < p < 1:
        return -float("inf")
    return successes * math.log(p) + (trials - successes) * math.log1p(-p)

def simulations():
    rng = np.random.default_rng(SEED)
    observations = rng.exponential(scale=1., size=10000)
    lln = [{"n": n, "sample_mean": float(observations[:n].mean())} for n in [10, 100, 1000, 10000]]
    clt = []
    histograms = []
    for n in [5, 30, 100]:
        means = rng.exponential(scale=1., size=(5000, n)).mean(axis=1)
        standardized = np.sqrt(n) * (means - 1.)  # population SD is 1
        counts, edges = np.histogram(standardized, bins=np.linspace(-4,4,33))
        histograms.append({"sample_size": n, "counts": counts.tolist(), "edges": edges.tolist(), "outside_range": int(len(standardized)-counts.sum())})
        clt.append({"sample_size": n, "replications": len(means),
                    "standardized_mean": float(standardized.mean()),
                    "standardized_variance": float(standardized.var(ddof=1)),
                    "standardized_skewness": float(stats.skew(standardized, bias=False)),
                    "fraction_in_minus1_96_to1_96": float(np.mean(np.abs(standardized) <= 1.96))})
    return {"seed": SEED, "population": "Exponential(rate=1), mean=1, variance=1; independent draws",
            "lln_one_running_sequence": lln, "clt_repeated_samples": clt, "clt_histograms": histograms,
            "caveat": "LLN does not promise monotone improvement; CLT concerns the sampling distribution of a standardized mean, not normal raw observations. These finite simulations illustrate, not prove, the theorems."}

def run():
    return {"chapter": "V1C04", "case_id": "V1C04-CASE01", "synthetic": True,
            "sample": SAMPLE, "inference": mean_inference(SAMPLE),
            "mle": {"bernoulli_successes": 7, "bernoulli_trials": 10, "bernoulli_p_hat": 0.7,
                    "log_likelihood_at_05": bernoulli_log_likelihood(.5), "log_likelihood_at_07": bernoulli_log_likelihood(.7),
                    "log_likelihood_at_09": bernoulli_log_likelihood(.9),
                    "normal_mean_hat": float(SAMPLE.mean()), "normal_variance_mle_ddof0": float(SAMPLE.var(ddof=0)),
                    "unbiased_sample_variance_ddof1": float(SAMPLE.var(ddof=1))},
            "simulations": simulations()}

if __name__ == "__main__":
    emit("V1C04", run())
