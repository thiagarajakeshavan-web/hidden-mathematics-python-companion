"""V1C02-CASE01: chain rule, gradients, finite differences and update size."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from common import emit

THETA = np.array([0.5, 0.5, 2.0, 0.0])  # w, b, v, c

def f(w):
    return (2 * w - 3) ** 2

def derivative(w):
    return 4 * (2 * w - 3)

def network(theta, x=2.0, target=4.0):
    w, b, v, c = np.asarray(theta, dtype=float)
    z = w * x + b
    h = max(z, 0.0)
    prediction = v * h + c
    error = prediction - target
    # The convention at the ReLU kink z=0 is zero; this point is not differentiable.
    local = 1.0 if z > 0 else 0.0
    gradient = np.array([error * v * local * x, error * v * local, error * h, error])
    return {"z": float(z), "h": float(h), "prediction": float(prediction),
            "loss": float(error ** 2 / 2), "gradient": gradient}

def finite_difference(fun, point, step=1e-5):
    point = np.asarray(point, dtype=float)
    result = np.empty_like(point)
    for i in range(len(point)):
        delta = np.zeros_like(point)
        delta[i] = step
        result[i] = (fun(point + delta) - fun(point - delta)) / (2 * step)
    return result

def run():
    initial = network(THETA)
    updates = []
    for rate in [0.01, 0.1]:
        theta_new = THETA - rate * initial["gradient"]  # simultaneous update
        updates.append({"learning_rate": rate, "parameters": theta_new, **network(theta_new)})
    numeric = finite_difference(lambda theta: network(theta)["loss"], THETA)
    return {"chapter": "V1C02", "case_id": "V1C02-CASE01", "synthetic": True,
            "scalar": {"w": 1., "f_w": f(1.), "analytic_derivative": derivative(1.),
                       "central_difference": float((f(1. + 1e-5) - f(1. - 1e-5)) / 2e-5)},
            "parameter_order": ["w", "b", "v", "c"], "initial_parameters": THETA,
            "network_initial": initial, "central_difference_gradient": numeric,
            "maximum_gradient_error": float(np.max(np.abs(numeric - initial["gradient"]))),
            "simultaneous_updates": updates,
            "warning": "A correct negative gradient is local; a large step can increase loss. Finite differences at a ReLU kink do not verify differentiability."}

if __name__ == "__main__":
    emit("V1C02", run())
