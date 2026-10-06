"""Small SFT, DPO and LoRA mechanics; no pretrained or generative model."""
import math
import numpy as np
from .numerics import array, positive, softmax, softplus, sigmoid, central_gradient


def sft_step(logits, target, learning_rate):
    logits = array(logits, 1, "logits")
    if not isinstance(target, int) or not 0 <= target < len(logits):
        raise ValueError("target index out of range")
    eta = positive(learning_rate, "learning rate")
    p = softmax(logits)
    grad = p.copy(); grad[target] -= 1
    after = logits - eta * grad
    updated = softmax(after)
    # logsumexp formulation remains finite for extreme logits.
    def loss(z):
        m = np.max(z)
        return float(m + np.log(np.exp(z-m).sum()) - z[target])
    return {"probabilities_before": p, "loss_before": loss(logits), "gradient": grad,
            "logits_after": after, "probabilities_after": updated, "loss_after": loss(after)}


def dpo(pc, pr, rc, rr, beta):
    values = array([pc, pr, rc, rr], 1, "pair probabilities")
    if np.any(values <= 0) or np.any(values > 1) or pc+pr > 1+1e-12 or rc+rr > 1+1e-12:
        raise ValueError("chosen/rejected probabilities must be positive and fit a distribution")
    beta = positive(beta, "beta")
    reference_log_ratio = math.log(rc) - math.log(rr)
    log_ratio_delta = (math.log(pc) - math.log(pr)) - reference_log_ratio
    margin = beta * log_ratio_delta
    chosen_gradient = -beta * sigmoid(-margin)
    # Partial derivatives in log-probability coordinates, not unconstrained probabilities.
    grad = np.array([chosen_gradient, -chosen_gradient])
    numerical = central_gradient(lambda z: softplus(-beta*(z[0]-z[1]-reference_log_ratio)), np.log([pc, pr]))
    return {"log_ratio_delta": log_ratio_delta, "margin": margin, "loss": softplus(-margin),
            "log_probability_gradients": grad, "central_difference_gradients": numerical,
            "max_gradient_error": float(np.max(np.abs(grad-numerical)))}


def lora(w, a, b, x, scale=1.0):
    w, a, b, x = array(w, 2), array(a, 2), array(b, 2), array(x, 1)
    scale = positive(scale, "scale")
    if a.shape[0] != b.shape[1] or b.shape[0] != w.shape[0] or a.shape[1] != w.shape[1] or len(x) != w.shape[1]:
        raise ValueError("LoRA requires W[out,in], A[rank,in], B[out,rank], x[in]")
    update = scale * (b @ a)
    return {"base_output": w @ x, "weight_update": update, "adapter_output": update @ x,
            "combined_output": (w+update) @ x, "base_parameter_count": w.size,
            "adapter_parameter_count": a.size + b.size}


def run(i):
    s, d, l = i["sft"], i["dpo"], i["lora"]
    return {"sft": sft_step(s["logits"], s["preferred_index"], s["learning_rate"]),
            "dpo": dpo(d["policy_chosen"], d["policy_rejected"], d["reference_chosen"], d["reference_rejected"], d["beta"]),
            "lora": lora(l["W"], l["A"], l["B"], l["x"], l["scale"])}
