"""V1C07-CASE01: exact bias-variance and a held-out regularization experiment."""
from pathlib import Path
import math
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from common import emit

SEED = 707
NOISE_SD = 0.25

def exact_decomposition(predictions, truth=10.0, noises=(-2.0, 2.0)):
    predictions, noises = np.asarray(predictions), np.asarray(noises)
    if not np.isclose(noises.mean(), 0.0):
        raise ValueError("This demonstration requires zero-mean independent future noise.")
    mean_prediction = float(predictions.mean())
    bias_squared = (mean_prediction - truth) ** 2
    variance = float(np.mean((predictions - mean_prediction) ** 2))
    noise_variance = float(np.mean(noises ** 2))
    direct_mse = float(np.mean((predictions[:, None] - (truth + noises[None, :])) ** 2))
    return {"predictions": predictions, "truth": truth, "noise_values": noises,
            "bias_squared": bias_squared, "variance": variance, "noise_variance": noise_variance,
            "expected_squared_error": direct_mse, "sum_of_components": bias_squared + variance + noise_variance}

def model(degree, alpha=0.0):
    # Both feature expansion and scaling are fitted only on training rows.
    return make_pipeline(PolynomialFeatures(degree, include_bias=False), StandardScaler(),
                         LinearRegression() if alpha == 0 else Ridge(alpha=alpha))

def sample(rng, n):
    x = rng.uniform(-1, 1, (n, 1))
    return x, x[:, 0] ** 2 + rng.normal(0, NOISE_SD, n)

def regularization_experiment():
    rng = np.random.default_rng(SEED)
    x_train, y_train = sample(rng, 25)
    x_valid, y_valid = sample(rng, 200)
    # Test rows are generated independently, and never used for selecting alpha.
    x_test, y_test = sample(rng, 1000)
    candidates = [0.0, 1e-6, 1e-4, 0.01, 1.0, 100.0]
    validation = []
    fitted = {}
    for alpha in candidates:
        m = model(12, alpha).fit(x_train, y_train)
        fitted[alpha] = m
        validation.append({"alpha": alpha, "validation_mse": float(mean_squared_error(y_valid, m.predict(x_valid)))})
    selected = min(validation, key=lambda row: row["validation_mse"])["alpha"]
    comparisons = {}
    for name, m in {"degree_1_baseline": model(1).fit(x_train, y_train),
                    "degree_2_baseline": model(2).fit(x_train, y_train),
                    "degree_12_unregularized": fitted[0.0],
                    "degree_12_validation_selected": fitted[selected]}.items():
        comparisons[name] = {"train_mse": float(mean_squared_error(y_train, m.predict(x_train))),
                             "test_mse": float(mean_squared_error(y_test, m.predict(x_test)))}
    return {"seed": SEED, "data": "y=x^2+Normal(0,0.25^2), x~Uniform(-1,1)",
            "split_sizes": {"train": 25, "validation": 200, "test": 1000},
            "validation_scores": validation, "selected_alpha": selected,
            "comparisons": comparisons, "test_policy": "Select alpha on validation only; inspect test once for final illustrative comparisons."}

def ensemble_experiment(alpha, repetitions=150):
    rng = np.random.default_rng(SEED + 1)
    grid = np.linspace(-0.95, 0.95, 101).reshape(-1, 1)
    truth = grid[:, 0] ** 2
    predictions = {name: [] for name in ["degree_1", "degree_2", "degree_12", "degree_12_ridge"]}
    for _ in range(repetitions):
        x, y = sample(rng, 25)
        for name, degree, strength in [("degree_1", 1, 0), ("degree_2", 2, 0),
                                       ("degree_12", 12, 0), ("degree_12_ridge", 12, alpha)]:
            predictions[name].append(model(degree, strength).fit(x, y).predict(grid))
    results = {}
    for name, rows in predictions.items():
        p = np.asarray(rows)
        bias_squared = float(np.mean((p.mean(axis=0) - truth) ** 2))
        variance = float(np.mean(np.var(p, axis=0, ddof=0)))
        direct = float(np.mean((p - truth) ** 2))
        results[name] = {"bias_squared": bias_squared, "variance": variance,
                         "error_to_noiseless_truth": direct,
                         "expected_error_with_independent_noise": bias_squared + variance + NOISE_SD ** 2,
                         "decomposition_residual": direct - bias_squared - variance}
    return {"seed": SEED + 1, "repetitions": repetitions, "grid_points": len(grid),
            "noise_variance": NOISE_SD ** 2, "note": "Finite-ensemble estimates, not population guarantees. Ridge alpha fixed before this experiment.",
            "models": results}

def scalar_penalties(z, strength=1.0):
    if strength < 0:
        raise ValueError("Penalty strength cannot be negative.")
    return {"z": z, "lambda": strength,
            "l1_solution": float(np.sign(z) * max(abs(z)-strength,0.)),
            "l2_solution": z/(1+strength),
            "objectives": "L1: (w-z)^2/2+lambda*abs(w); L2: (w-z)^2/2+lambda*w^2/2"}

def run():
    reg = regularization_experiment()
    return {"chapter": "V1C07", "case_id": "V1C07-CASE01", "synthetic": True,
            "scalar_penalties": [scalar_penalties(3.), scalar_penalties(.6)],
            "exact_unbiased": exact_decomposition([8, 10, 12]),
            "exact_biased": exact_decomposition([8, 8, 8]),
            "hoeffding": {"n": 1000, "delta": 0.05, "single_fixed_hypothesis_epsilon": math.sqrt(math.log(2 / 0.05) / 2000),
                          "100_hypotheses_uniform_epsilon": math.sqrt(math.log(200 / 0.05) / 2000),
                          "required_n_M100_epsilon_005": math.ceil(math.log(200 / 0.05) / (2 * 0.05 ** 2)),
                          "assumptions": "Independent identically distributed examples; loss in [0,1]; finite hypothesis family fixed independently of the evaluation sample."},
            "regularization": reg, "repeated_fits": ensemble_experiment(reg["selected_alpha"])}

if __name__ == "__main__":
    emit("V1C07", run())
