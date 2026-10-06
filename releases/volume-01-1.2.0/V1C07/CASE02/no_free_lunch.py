"""V1C07-CASE02: a finite illustration of a No Free Lunch symmetry.

A fixed observed point a and an unseen point b have uniformly weighted binary
labels. This is a toy conditional enumeration, not a real-data benchmark or a
proof that practical algorithms are equally good.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def consistent_targets(observed_label=0):
    if type(observed_label) is not int or observed_label not in (0, 1):
        raise ValueError("The observed binary label must be integer 0 or 1.")
    return [labels for labels in product((0, 1), repeat=2) if labels[0] == observed_label]


def mean_unseen_error(predicted_label, observed_label=0):
    if type(predicted_label) is not int or predicted_label not in (0, 1):
        raise ValueError("The predicted binary label must be integer 0 or 1.")
    targets = consistent_targets(observed_label)
    return Fraction(sum(predicted_label != labels[1] for labels in targets), len(targets))


def randomized_unseen_error(probability_predict_one):
    q = probability_predict_one
    if isinstance(q, bool) or not isinstance(q, (int, Fraction)) or not 0 <= q <= 1:
        raise ValueError("Use an exact integer or Fraction probability between 0 and 1.")
    return Fraction(1, 2) * q + Fraction(1, 2) * (1 - q)


def encoded(value):
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": float(value)}


def run():
    return {"case_id": "V1C07-CASE02", "domain": ["a", "b"],
            "observed": {"a": 0}, "unseen_point": "b",
            "consistent_targets": [list(t) for t in consistent_targets()],
            "target_probabilities": [encoded(Fraction(1, 2)), encoded(Fraction(1, 2))],
            "always_predict_zero_mean_unseen_error": encoded(mean_unseen_error(0)),
            "always_predict_one_mean_unseen_error": encoded(mean_unseen_error(1)),
            "randomized_predict_one_probability": encoded(Fraction(1, 4)),
            "randomized_mean_unseen_error": encoded(randomized_unseen_error(Fraction(1, 4))),
            "assumptions": "Fixed observed subset, uniform weighting over all binary target functions consistent with the observation, unseen-point 0-1 loss, no restriction favouring a particular target pattern.",
            "scope": "A finite symmetry illustration. Real datasets are not generally uniform over all target functions, and useful inductive biases can perform differently on structured tasks. This does not say every practical learner is equally good or that learning is pointless."}


def main():
    result = run()
    (Path(__file__).resolve().parent / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
