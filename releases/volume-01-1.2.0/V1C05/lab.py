"""V1C05-CASE01: gradient descent and conditioning; all data synthetic."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from common import emit

X = np.array([1.0, 2.0])
Y = np.array([2.0, 4.0])

def loss(w):
    return float(np.mean((X * w - Y) ** 2) / 2)

def gradient(w):
    return float(np.mean(X * (X * w - Y)))

def descent(rate, steps=8):
    w = 0.0
    rows = []
    for k in range(steps + 1):
        rows.append({"iteration": k, "w": w, "loss": loss(w), "gradient": gradient(w)})
        w -= rate * gradient(w)
    return rows

def conditioned_descent(steps=100):
    hessian = np.diag([1.0, 100.0])
    raw = np.ones(2)
    scaled = raw.copy()
    history = []
    for k in range(steps + 1):
        history.append({"iteration": k, "raw_loss": float(raw @ hessian @ raw / 2),
                        "preconditioned_loss": float(scaled @ hessian @ scaled / 2)})
        raw -= 0.01 * (hessian @ raw)
        # Multiplication by inverse diagonal curvature is diagonal preconditioning.
        scaled -= 0.5 * np.linalg.solve(hessian, hessian @ scaled)
    return {"hessian": hessian.tolist(), "condition_number": float(np.linalg.cond(hessian)),
            "raw_learning_rate": 0.01, "preconditioned_learning_rate": 0.5,
            "history": history}

def run():
    conditioning = conditioned_descent()
    return {"chapter": "V1C05", "case_id": "V1C05-CASE01", "synthetic": True,
            "x": X, "y": Y, "loss_convention": "mean squared error / 2",
            "stable_rate_interval": "0 < alpha < 0.8 for this quadratic",
            "gradient_checks": [{"step": h, "central_difference_at_zero": (loss(h)-loss(-h))/(2*h)} for h in [1e-3,1e-5,1e-7]],
            "individual_gradients_at_zero": X * (X * 0.0 - Y),
            "full_gradient_at_zero": gradient(0.),
            "stable": descent(0.2, 4), "boundary_oscillation": descent(0.8, 4),
            "divergence": descent(1.0, 8), "conditioning": conditioning}

if __name__ == "__main__":
    emit("V1C05", run())
