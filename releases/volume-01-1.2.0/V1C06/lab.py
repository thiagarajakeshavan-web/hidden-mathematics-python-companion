"""V1C06-CASE01: entropy, cross-entropy, KL and stable softmax."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.special import logsumexp
from common import emit

def distribution(p):
    p = np.asarray(p, dtype=float)
    if p.ndim != 1 or not np.all(np.isfinite(p)) or np.any(p < 0) or not np.isclose(p.sum(), 1):
        raise ValueError("Expected a finite nonnegative probability vector summing to one.")
    return p

def entropy(p, base=2.0):
    if not np.isfinite(base) or base <= 0 or base == 1:
        raise ValueError("Logarithm base must be positive, finite and unequal to one.")
    p = distribution(p)
    positive = p > 0
    return float(-np.sum(p[positive] * np.log(p[positive])) / np.log(base))

def cross_entropy(p, q, base=2.0):
    if not np.isfinite(base) or base <= 0 or base == 1:
        raise ValueError("Logarithm base must be positive, finite and unequal to one.")
    p, q = distribution(p), distribution(q)
    if p.shape != q.shape:
        raise ValueError("Distributions must have the same support shape.")
    positive = p > 0
    if np.any(q[positive] == 0):
        return float("inf")
    return float(-np.sum(p[positive] * np.log(q[positive])) / np.log(base))

def kl_divergence(p, q, base=2.0):
    return cross_entropy(p, q, base) - entropy(p, base)

def stable_softmax(logits):
    logits = np.asarray(logits, dtype=float)
    return np.exp(logits - logsumexp(logits))

def mutual_information(joint):
    joint = np.asarray(joint, dtype=float)
    if joint.ndim != 2 or np.any(joint < 0) or not np.isclose(joint.sum(), 1):
        raise ValueError("Expected a normalized nonnegative joint-probability table.")
    independent = joint.sum(axis=1)[:, None] * joint.sum(axis=0)[None, :]
    positive = joint > 0
    return float(np.sum(joint[positive] * np.log2(joint[positive] / independent[positive])))

def information_extension():
    joint = np.array([[.4,.1],[.1,.4]])
    rng = np.random.default_rng(606)
    samples = []
    for n in [100, 1000, 10000]:
        counts = rng.multinomial(n, joint.ravel()).reshape(2,2)
        samples.append({"n": n, "cell_counts": counts, "estimated_mi_bits": mutual_information(counts/n)})
    xor_pair_joint = np.array([[.25,0],[0,.25],[0,.25],[.25,0]])
    return {"joint_table": joint, "mutual_information_bits": mutual_information(joint),
            "seed": 606, "sample_estimates": samples,
            "xor": {"I_X1_Y_bits": mutual_information(np.full((2,2),.25)),
                    "I_X2_Y_bits": mutual_information(np.full((2,2),.25)),
                    "I_pair_Y_bits": mutual_information(xor_pair_joint)},
            "note": "Plug-in estimates fluctuate and are biased at small sample sizes; XOR has useful pairwise interaction despite zero univariate information."}

def run():
    p = np.array([0.75, 0.25])
    q = np.array([0.6, 0.4])
    logits = np.array([1000.0, 1001.0, 999.0])
    normalizer = float(logsumexp(logits))
    return {"chapter": "V1C06", "case_id": "V1C06-CASE01", "synthetic": True,
            "p": p, "q": q, "entropy_bits": entropy(p),
            "cross_entropy_bits": cross_entropy(p, q), "kl_bits": kl_divergence(p, q),
            "reverse_kl_bits": kl_divergence(q, p), "logits": logits,
            "logsumexp": normalizer, "softmax": stable_softmax(logits),
            "true_class_index_zero_based": 1, "true_class_loss_nats": normalizer - logits[1],
            "logit_gradient": stable_softmax(logits)-np.array([0.,1.,0.]),
            "single_token_perplexity": float(np.exp(normalizer-logits[1])),
            "mutual_information_extension": information_extension(),
            "zero_support_cross_entropy_is_infinite": bool(np.isinf(cross_entropy([1, 0], [0, 1]))),
            "identity_residual_bits": cross_entropy(p, q) - entropy(p) - kl_divergence(p, q)}

if __name__ == "__main__":
    emit("V1C06", run())
