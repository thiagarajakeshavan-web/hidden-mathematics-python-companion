"""V1C04-CASE02: exact Bernoulli MLE and interior Beta-prior MAP bridge."""
from fractions import Fraction
import json
from pathlib import Path


def estimate(successes=7, trials=10, prior_alpha=2, prior_beta=2):
    values = (successes, trials, prior_alpha, prior_beta)
    if any(type(x) is not int for x in values) or trials <= 0 or not 0 <= successes <= trials or prior_alpha <= 0 or prior_beta <= 0:
        raise ValueError("Use valid integer counts and positive integer Beta parameters.")
    alpha, beta = prior_alpha + successes, prior_beta + trials - successes
    if alpha <= 1 or beta <= 1:
        raise ValueError("The interior posterior mode formula requires both posterior parameters > 1; boundary modes need separate treatment.")
    return {"successes": successes, "trials": trials,
            "prior_alpha": prior_alpha, "prior_beta": prior_beta,
            "posterior_alpha": alpha, "posterior_beta": beta,
            "mle": Fraction(successes, trials), "map": Fraction(alpha - 1, alpha + beta - 2),
            "posterior_mean": Fraction(alpha, alpha + beta)}


def run():
    def encoded(alpha, beta):
        return {key: {"numerator": value.numerator, "denominator": value.denominator, "decimal": float(value)}
                if isinstance(value, Fraction) else value
                for key, value in estimate(prior_alpha=alpha, prior_beta=beta).items()}
    return {"case_id": "V1C04-CASE02", "data_status": "Ten constructed Bernoulli trials with seven successes.",
            "beta_2_2_prior": encoded(2, 2), "uniform_beta_1_1_prior": encoded(1, 1),
            "scope": "MLE maximises likelihood; MAP maximises posterior density under the stated parameterisation. The posterior mean is a third distinct estimate. An interior Beta(a,b) mode uses (a-1)/(a+b-2) only if a>1 and b>1. Prior choice is illustrative, not evidence of better predictive performance."}


def main():
    output = run()
    (Path(__file__).resolve().parent / "results.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output))


if __name__ == "__main__":
    main()
