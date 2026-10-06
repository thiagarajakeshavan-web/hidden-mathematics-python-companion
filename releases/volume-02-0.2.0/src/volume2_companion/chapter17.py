"""Scaled dot-product attention, causal masking and sinusoidal positions."""
import math
import numpy as np
from .numerics import array, softmax


def attention(q, k, v, causal=True):
    q, k, v = array(q, 2, "Q"), array(k, 2, "K"), array(v, 2, "V")
    if q.shape[1] != k.shape[1] or k.shape[0] != v.shape[0]:
        raise ValueError("Q/K feature dimensions and K/V token dimensions must match")
    if causal and q.shape[0] != k.shape[0]:
        raise ValueError("this self-attention lab requires equal Q and K token counts")
    scores = q @ k.T / math.sqrt(q.shape[1])
    allowed = np.tri(*scores.shape, dtype=bool) if causal else None
    weights = softmax(scores, allowed)
    return scores, weights, weights @ v


def sinusoidal(positions, dimension):
    p = array(positions, 1, "positions")
    if not isinstance(dimension, int) or dimension <= 0 or dimension % 2:
        raise ValueError("position dimension must be a positive even integer")
    frequencies = 10000.0 ** (-np.arange(0, dimension, 2) / dimension)
    angle = p[:, None] * frequencies[None, :]
    result = np.empty((p.size, dimension))
    result[:, 0::2], result[:, 1::2] = np.sin(angle), np.cos(angle)
    return result


def run(i):
    if len(i["Q"][0]) != i["key_dimension"]:
        raise ValueError("declared key dimension does not match data")
    scores, weights, out = attention(i["Q"], i["K"], i["V"])
    _, unmasked, unmasked_out = attention(i["Q"], i["K"], i["V"], False)
    return {"scores": scores, "causal_weights": weights, "causal_output": out,
            "unmasked_weights": unmasked, "unmasked_output": unmasked_out,
            "sinusoidal_positions": sinusoidal(i["positions"], i["position_dimension"])}
