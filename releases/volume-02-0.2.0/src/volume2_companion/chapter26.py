"""Offline distribution drift, error budgets, Little's law and analytic latency."""
import math
from decimal import Decimal
import numpy as np
from .numerics import probabilities, positive, array


def total_variation(reference, current):
    p, q = probabilities(reference), probabilities(current)
    if p.shape != q.shape:
        raise ValueError("distributions require matching bins")
    return float(0.5*np.abs(p-q).sum())


def error_budget(requests, bad, target):
    if not isinstance(requests, int) or isinstance(requests, bool) or requests <= 0 or not isinstance(bad, int) or isinstance(bad, bool) or not 0 <= bad <= requests:
        raise ValueError("need integer 0 <= bad <= requests with requests > 0")
    if not math.isfinite(target) or not 0 < target < 1:
        raise ValueError("target must lie strictly between zero and one")
    allowed = float(Decimal(requests)*(Decimal(1)-Decimal(str(target))))
    return {"availability": 1-bad/requests, "allowed_bad_requests": allowed,
            "remaining_budget": allowed-bad, "budget_burn_fraction": bad/allowed}


def nearest_rank(values, quantile):
    v = array(values, 1, "latencies")
    if np.any(v < 0) or not math.isfinite(quantile) or not 0 < quantile <= 1:
        raise ValueError("nonnegative latencies and quantile in (0,1] required")
    return float(np.sort(v)[math.ceil(len(v)*quantile)-1])


def run(i):
    rate = positive(i["arrival_rate_per_second"], "arrival rate", allow_zero=True)
    seconds = positive(i["mean_service_seconds"], "mean service seconds", allow_zero=True)
    baseline = sum(positive(i[k], k, allow_zero=True) for k in ("single_request_gpu_ms", "cpu_ms", "transfer_ms"))
    candidate = sum(positive(i[k], k, allow_zero=True) for k in ("candidate_gpu_ms", "cpu_ms", "transfer_ms"))
    if baseline <= 0 or candidate <= 0:
        raise ValueError("total latency must be positive")
    return {"total_variation": total_variation(i["reference_mix"], i["current_mix"]),
            **error_budget(i["requests"], i["bad_requests"], i["availability_target"]),
            "mean_concurrency": rate*seconds, "baseline_total_ms": baseline,
            "candidate_total_ms": candidate, "speedup": baseline/candidate,
            "scope": "Synthetic counts and assumed component times; no running service or GPU benchmark."}
