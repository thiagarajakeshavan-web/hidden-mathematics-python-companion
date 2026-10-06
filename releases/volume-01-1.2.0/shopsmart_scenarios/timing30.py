"""V1C10-CASE03: scenario-based buy-today / wait-two / wait-three decision.

This is decision arithmetic using ASSUMED scenarios, not a learned forecast.
The chosen day is decided now; store allocation is selected after that day's
prices/stock are observed. Expected adaptive cost is not a guaranteed quote.
"""
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shopsmart_scenarios.grocery30 import HERE, STORES, integer, load_catalogue, solve


def load_scenarios():
    return json.loads((HERE / "data" / "timing_scenarios.json").read_text(encoding="utf-8"))


def scenario_rows(rows, day, state, promotions):
    result = deepcopy(rows)
    by_id = {row["item_id"]: row for row in result}
    delta = state["nonpromotion_pack_delta_cents"]
    if type(delta) is not int:
        raise ValueError("Scenario price delta must be integer cents.")
    for row in result:
        for offer in row["offers"]:
            offer["price_cents"] += delta
            if offer["price_cents"] < 0:
                raise ValueError("A scenario produces a negative price.")
    applied = []
    for promotion in promotions:
        if promotion["evidence_status"] != "CONFIRMED_WITHIN_FICTION_ONLY":
            raise ValueError("This fixture accepts fictional promotion evidence only; live evidence is not implemented.")
        if promotion["valid_from_day"] <= day <= promotion["valid_to_day"]:
            by_id[promotion["item_id"]]["offers"][STORES.index(promotion["store"])]["price_cents"] = promotion["price_cents"]
            applied.append(promotion["promotion_id"])
    for change in state["stock_overrides"]:
        by_id[change["item_id"]]["offers"][STORES.index(change["store"])]["stock_packs"] = change["stock_packs"]
    return result, applied


def rational(value):
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": float(value)}


def run(*, need_by_day=None, waiting_cost_per_day_cents=None, scenarios=None):
    spec = load_scenarios() if scenarios is None else deepcopy(scenarios)
    deadline = spec["need_by_day"] if need_by_day is None else need_by_day
    waiting = spec["waiting_cost_per_day_cents"] if waiting_cost_per_day_cents is None else waiting_cost_per_day_cents
    integer(deadline, "need-by day")
    integer(waiting, "daily waiting cost")
    rows = load_catalogue()
    today = solve(rows)
    now = today["best_plan"]["payable_cents"]
    days = [{"day": 0, "eligible_by_deadline": True, "status": "complete_in_synthetic_observed_fixture",
             "expected_payable_cents": rational(Fraction(now)), "waiting_cost_cents": 0,
             "expected_decision_cost_cents": rational(Fraction(now)), "net_expected_saving_vs_today_cents": rational(Fraction(0)),
             "scenario_payable_range_cents": [now, now], "worst_case_decision_cost_cents": now,
             "states": [{"name": "synthetic_today", "probability_basis_points": 10000, "optimization": today}]}]
    seen_days = {0}
    for day_input in spec["future_days"]:
        day = integer(day_input["day"], "future day", 1)
        if day in seen_days:
            raise ValueError("Future days must be unique.")
        seen_days.add(day)
        states = day_input["states"]
        if not states:
            raise ValueError("Each future day needs at least one state.")
        if any(type(x["probability_basis_points"]) is not int or x["probability_basis_points"] <= 0 for x in states) or sum(x["probability_basis_points"] for x in states) != 10000:
            raise ValueError("Positive state probability basis points must sum to 10000.")
        outputs, expected, totals = [], Fraction(0), []
        infeasible_probability = 0
        for state in states:
            future, applied = scenario_rows(rows, day, state, spec["promotions"])
            answer = solve(future)
            probability = Fraction(state["probability_basis_points"], 10000)
            if answer["best_plan"] is None:
                infeasible_probability += state["probability_basis_points"]
            else:
                total = answer["best_plan"]["payable_cents"]
                expected += probability * total
                totals.append(total)
            outputs.append({"name": state["name"], "probability_basis_points": state["probability_basis_points"],
                            "price_status": "scenario_forecast_except_explicit_fictional_promotions",
                            "applied_fictional_promotion_ids": applied, "optimization": answer})
        # Do not average only surviving baskets or silently price unmet demand at zero.
        complete = infeasible_probability == 0
        decision = expected + day * waiting if complete else None
        days.append({"day": day, "eligible_by_deadline": day <= deadline,
                     "status": "complete_in_all_assumed_scenarios" if complete else "infeasible_scenario_blocks_comparison",
                     "infeasible_probability_basis_points": infeasible_probability,
                     "expected_payable_cents": rational(expected) if complete else None,
                     "waiting_cost_cents": day * waiting,
                     "expected_decision_cost_cents": rational(decision) if complete else None,
                     "net_expected_saving_vs_today_cents": rational(Fraction(now) - decision) if complete else None,
                     "scenario_payable_range_cents": [min(totals), max(totals)] if complete else None,
                     "worst_case_decision_cost_cents": max(totals) + day * waiting if complete else None,
                     "states": outputs})
    candidates = [d for d in days if d["eligible_by_deadline"] and d["expected_decision_cost_cents"] is not None]
    chosen = min(candidates, key=lambda d: (Fraction(d["expected_decision_cost_cents"]["numerator"], d["expected_decision_cost_cents"]["denominator"]), d["day"]))
    robust = min(candidates, key=lambda d: (d["worst_case_decision_cost_cents"], d["day"]))
    return {"case_id": "V1C10-CASE03", "currency": "AUD", "need_by_day": deadline,
            "data_status": spec["data_status"], "waiting_cost_per_day_cents": waiting,
            "days": days, "risk_neutral_selected_day": chosen["day"], "minimax_selected_day": robust["day"],
            "forecast_horizons_days": sorted(seen_days - {0}),
            "interpretation": "Ranges are an assumed discrete scenario envelope, not statistical prediction intervals. Expectation uses joint scenario weights; it does not assume independent item-price changes. Waiting cost is a preference penalty, not a checkout fee. Same-day store allocation adapts after prices are observed. Confirmed means confirmed only inside this invented fixture. No future discount, stock, service or saving is guaranteed. Missing scenarios and expiry/quality risks remain unmodelled; refresh evidence before any real decision."}


def main():
    result = run()
    (HERE / "timing30_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"case": result["case_id"], "risk_neutral_selected_day": result["risk_neutral_selected_day"],
                      "minimax_selected_day": result["minimax_selected_day"],
                      "decision_costs_cents": {d["day"]: d["expected_decision_cost_cents"] for d in result["days"]}}))


if __name__ == "__main__":
    main()
