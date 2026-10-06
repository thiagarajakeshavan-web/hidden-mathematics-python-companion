"""One ReLU hidden neuron; exact backpropagation and a finite-difference audit."""
import numpy as np
from .numerics import array, sigmoid, softplus, positive, central_gradient


def forward(theta, x, y):
    x = array(x, ndim=1, name="features")
    theta = array(theta, ndim=1, name="parameters")
    if theta.size != x.size + 3 or y not in (0, 1):
        raise ValueError("expected feature weights plus b,v,c and binary target")
    w, b, v, c = theta[:-3], theta[-3], theta[-2], theta[-1]
    z = float(w @ x + b)
    h = max(0.0, z)
    a = float(v * h + c)
    p = sigmoid(a)
    return {"z": z, "h": h, "a": a, "probability": p,
            "loss": softplus(a) - y * a}


def gradient(theta, x, y):
    r = forward(theta, x, y)
    delta = r["probability"] - y
    dz = delta * theta[-2] * float(r["z"] > 0)
    return np.r_[dz * np.asarray(x), dz, delta * r["h"], delta]


def run(inputs):
    i = inputs
    theta = np.r_[i["w"], i["b"], i["v"], i["c"]]
    eta = positive(i["learning_rate"], "learning rate")
    r = forward(theta, i["x"], i["y"])
    g = gradient(theta, i["x"], i["y"])
    numerical = central_gradient(lambda t: forward(t, i["x"], i["y"])["loss"], theta, i["epsilon"])
    updated = theta - eta * g  # simultaneous update from ORIGINAL parameters
    after = forward(updated, i["x"], i["y"])
    return {**r, "analytic_gradients": g, "central_difference_gradients": numerical,
            "max_gradient_error": float(np.max(np.abs(g - numerical))),
            "updated_parameters": updated, "updated_probability": after["probability"],
            "updated_loss": after["loss"]}
