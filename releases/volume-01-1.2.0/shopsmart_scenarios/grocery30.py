"""V1C05-CASE03: exact whole-line, whole-pack allocation over three stores.

All commercial inputs are synthetic. This code never connects to retailers or
couriers. A DP state retains the cheapest allocation for an EXACT used-store
mask. Fixed per-mask fees are then added, yielding every feasible store subset.
Complexity O(number_of_lines * number_of_stores * 2**number_of_stores), apart
from retaining the short assignment path. It does not enumerate 3**30 baskets.
"""
from copy import deepcopy
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORES = ("Coles", "Woolworths", "ALDI")
STORE_KEYS = ("coles", "woolworths", "aldi")
ROUTE_CHECKS = ("service_area", "pickup_available", "windows_overlap",
                "route_time_valid", "cold_chain_capable")


def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}.")
    return value


def load_catalogue(path=HERE / "data" / "grocery30.csv"):
    rows = []
    with Path(path).open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["cold_chain"] not in ("true", "false"):
                raise ValueError("CSV cold_chain must be explicit true or false; unknown cannot become False.")
            rows.append({"item_id": row["item_id"], "name": row["name"],
                         "unit": row["unit"], "required": int(row["required"]),
                         "cold_chain": row["cold_chain"] == "true",
                         "offers": [{"store": name, "pack": int(row[f"{key}_pack"]),
                                     "price_cents": int(row[f"{key}_price_cents"]),
                                     "stock_packs": int(row[f"{key}_stock"]),
                                     "equivalence_approved": True}
                                    for name, key in zip(STORES, STORE_KEYS)]})
    validate_rows(rows)
    return rows


def default_routes():
    # No membership, coupon, minimum spend, free-shipping threshold or hidden tax.
    # These assumed all-in fees already include all mandatory charges in this toy model.
    routes = {}
    for mask in range(1, 8):
        n = mask.bit_count()
        if n == 1:
            delivery = {1: 600, 2: 650, 4: 500}[mask]
            fee = {"delivery_cents": delivery, "handling_cents": 0,
                   "extra_stop_cents": 0, "other_mandatory_cents": 0}
        else:
            fee = {"delivery_cents": 800, "handling_cents": 100 * n,
                   "extra_stop_cents": 200 * (n - 1), "other_mandatory_cents": 0}
        routes[mask] = {**fee, **{key: True for key in ROUTE_CHECKS},
                        "minimum_spend_cents": 0, "membership_required": False}
    return routes


def validate_rows(rows):
    if not rows:
        raise ValueError("At least one requested line is required.")
    seen = set()
    for row in rows:
        if not isinstance(row["item_id"], str) or not row["item_id"] or row["item_id"] in seen:
            raise ValueError("Item IDs must be nonempty and unique.")
        seen.add(row["item_id"])
        integer(row["required"], "required quantity", 1)
        if row["unit"] not in ("g", "ml", "count", "slice", "bag"):
            raise ValueError("Unsupported or mismatched unit.")
        if type(row["cold_chain"]) is not bool:
            raise ValueError("cold_chain must be Boolean.")
        if len(row["offers"]) != 3:
            raise ValueError("Exactly one matched offer per store and line is required.")
        for index, offer in enumerate(row["offers"]):
            if offer["store"] != STORES[index]:
                raise ValueError("Offers must be ordered Coles, Woolworths, ALDI.")
            integer(offer["pack"], "pack quantity", 1)
            for field in ("price_cents", "stock_packs"):
                if offer[field] is not None:
                    integer(offer[field], field)
            if offer["equivalence_approved"] not in (True, False, None) or isinstance(offer["equivalence_approved"], int) and type(offer["equivalence_approved"]) is not bool:
                raise ValueError("Equivalence approval must be True, False, or None.")


def validate_routes(routes):
    if set(routes) != set(range(1, 8)):
        raise ValueError("Provide routes for all seven nonempty store masks.")
    for route in routes.values():
        for field in ("delivery_cents", "handling_cents", "extra_stop_cents", "other_mandatory_cents"):
            integer(route[field], field)
        integer(route["minimum_spend_cents"], "minimum spend")
        if route["minimum_spend_cents"] != 0 or route["membership_required"] is not False:
            raise ValueError("This fixed-fee teaching solver does not support minimum-spend or membership rules.")
        for field in ROUTE_CHECKS:
            if route[field] is not None and type(route[field]) is not bool:
                raise ValueError("Route eligibility must be True, False, or None.")


def line_option(row, store):
    offer = row["offers"][store]
    packs = (row["required"] + offer["pack"] - 1) // offer["pack"]
    if (offer["price_cents"] is None or offer["stock_packs"] is None
            or offer["stock_packs"] < packs or offer["equivalence_approved"] is not True):
        return None
    return {"item_id": row["item_id"], "name": row["name"], "store": STORES[store],
            "unit": row["unit"], "required": row["required"], "pack_size": offer["pack"],
            "packs": packs, "purchased_quantity": packs * offer["pack"],
            "surplus_quantity": packs * offer["pack"] - row["required"],
            "price_per_pack_cents": offer["price_cents"],
            "goods_cents": packs * offer["price_cents"]}


def route_reasons(route, rows):
    return [key for key in ROUTE_CHECKS
            if (key != "cold_chain_capable" or any(row["cold_chain"] for row in rows))
            and route[key] is not True]


def make_plan(rows, assignment, routes):
    if len(assignment) != len(rows):
        raise ValueError("Assignment must contain exactly one store per requested line.")
    for index in assignment:
        integer(index, "store index")
        if index >= 3:
            raise ValueError("Store index must be 0, 1, or 2.")
    mask = sum(1 << i for i in set(assignment))
    lines = [line_option(row, i) for row, i in zip(rows, assignment)]
    if any(line is None for line in lines) or route_reasons(routes[mask], rows):
        return None
    fees = {key: routes[mask][key] for key in
            ("delivery_cents", "handling_cents", "extra_stop_cents", "other_mandatory_cents")}
    goods = sum(line["goods_cents"] for line in lines)
    fee_total = sum(fees.values())
    return {"store_mask": mask, "stores": [STORES[i] for i in range(3) if mask & (1 << i)],
            "line_counts": {name: assignment.count(i) for i, name in enumerate(STORES)},
            "requested_line_count": len(rows), "purchased_pack_count": sum(x["packs"] for x in lines),
            "goods_cents": goods, "fee_breakdown": fees, "fees_cents": fee_total,
            "payable_cents": goods + fee_total, "lines": lines}


def solve(rows=None, routes=None, *, strict_budget_cents=None):
    rows = load_catalogue() if rows is None else deepcopy(rows)
    routes = default_routes() if routes is None else deepcopy(routes)
    validate_rows(rows)
    validate_routes(routes)
    if strict_budget_cents is not None:
        integer(strict_budget_cents, "strict budget", 1)
    # Keeping only the cheapest prefix per exact mask is sound because offers
    # are independent, each requested item has its own stock and all fees depend
    # only on the final used mask. Additive costs share the same future suffixes.
    states = {0: (0, ())}
    transitions = 0
    for row in rows:
        next_states = {}
        for mask, (cost, assignment) in states.items():
            for store in range(3):
                option = line_option(row, store)
                if option is None:
                    continue
                transitions += 1
                new_mask = mask | (1 << store)
                candidate = (cost + option["goods_cents"], assignment + (store,))
                if new_mask not in next_states or candidate < next_states[new_mask]:
                    next_states[new_mask] = candidate
        states = next_states
    subsets, feasible = [], []
    for mask in range(1, 8):
        missing = [row["item_id"] for row in rows
                   if not any(line_option(row, i) is not None for i in range(3) if mask & (1 << i))]
        reasons = route_reasons(routes[mask], rows)
        plan = make_plan(rows, list(states[mask][1]), routes) if mask in states and not reasons else None
        if plan is not None and strict_budget_cents is not None and plan["payable_cents"] >= strict_budget_cents:
            reasons.append("strict_budget_exceeded_or_equal")
            plan = None
        if plan is None and mask not in states:
            reasons.append("no_complete_allocation_using_exact_subset")
        subsets.append({"store_mask": mask, "stores": [STORES[i] for i in range(3) if mask & (1 << i)],
                        "feasible": plan is not None, "missing_item_ids": missing,
                        "reasons": reasons, "plan": plan})
        if plan is not None:
            feasible.append(plan)
    feasible.sort(key=lambda p: (p["payable_cents"], p["store_mask"], [x["store"] for x in p["lines"]]))
    return {"subsets": subsets, "best_plan": feasible[0] if feasible else None,
            "dp_transitions": transitions, "max_mask_states": 8,
            "naive_assignment_count_avoided": 3 ** len(rows)}


def run():
    rows = load_catalogue()
    result = solve(rows)
    fixed = make_plan(rows, [0] * 10 + [1] * 10 + [2] * 10, default_routes())
    single = {entry["stores"][0]: entry["plan"] for entry in result["subsets"] if len(entry["stores"]) == 1}
    best_single = min(p["payable_cents"] for p in single.values() if p is not None)
    return {"case_id": "V1C05-CASE03", "currency": "AUD", "money_unit": "integer cents",
            "data_status": "Entire catalogue, equivalence, availability and fees are synthetic assumptions; no live retailer or courier claims.",
            "input_line_count": len(rows), "single_store_plans": single,
            "fixed_10_10_10_plan": fixed, "optimization": result,
            "savings_vs_cheapest_single_cents": best_single - result["best_plan"]["payable_cents"],
            "fixed_split_excess_over_optimum_cents": fixed["payable_cents"] - result["best_plan"]["payable_cents"],
            "scope": "Each full requested line goes to one store. Whole packs may exceed requested quantity. All matched equivalents are explicitly assumed approved. No split of one line across stores, volume discounts, nonzero minimum spend or membership rules. No actual allergy eligibility is assessed in this general grocery case."}


def main():
    result = run()
    (HERE / "grocery30_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"case": result["case_id"], "best_payable_cents": result["optimization"]["best_plan"]["payable_cents"]}))


if __name__ == "__main__":
    main()
