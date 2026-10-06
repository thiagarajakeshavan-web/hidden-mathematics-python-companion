"""V1C05-CASE02: exact synthetic whole-pack basket/fee enumeration.

This additive case does not alter the original optimization lab. It implements
only teaching arithmetic: no live retailer prices, speech/OCR, substitutions,
orders, delivery booking or allergen-safety judgments.
"""
from pathlib import Path
import itertools
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from common import ROOT, plain

STORES = ("Coles", "Woolworths", "ALDI")
PRODUCTS = ("P1", "P2", "P3")
# Store rows, product columns; exact Australian cents, one whole pack per line.
PRICES_CENTS = np.array([[800, 1100, 1000], [1000, 700, 1200], [900, 1000, 600]])
SINGLE_STORE_FEES_CENTS = np.array([400, 700, 900])
PICKUP_PER_STORE_CENTS = 200
CONSOLIDATED_COURIER_CENTS = 800

def boolean_matrix(value, default, name):
    result = np.full((3, 3), default, dtype=bool) if value is None else np.asarray(value)
    if result.shape != (3, 3) or result.dtype.kind != "b":
        raise ValueError(f"{name} must be a 3x3 Boolean matrix (store rows, product columns).")
    return result

def enumerate_plans(*, budget_cents=4000, stock=None, product_eligible=None,
                    store_service_available=None, consolidated_service_available=True,
                    requires_substitution=None, approved_substitutions=None):
    """Enumerate all eligible assignments; exclude total >= strict budget.

    Availability/eligibility flags are supplied assumptions, not verified data.
    Unknown availability must be represented as False rather than guessed True.
    A flagged substitution is excluded unless its specific flag is approved.
    """
    if budget_cents is not None and (not isinstance(budget_cents, int) or isinstance(budget_cents, bool) or budget_cents <= 0):
        raise ValueError("Budget must be a positive integer number of cents, or None.")
    stock = boolean_matrix(stock, True, "stock")
    eligible = boolean_matrix(product_eligible, True, "product_eligible")
    substitute = boolean_matrix(requires_substitution, False, "requires_substitution")
    approved = boolean_matrix(approved_substitutions, False, "approved_substitutions")
    service = np.ones(3, dtype=bool) if store_service_available is None else np.asarray(store_service_available)
    if service.shape != (3,) or service.dtype.kind != "b" or not isinstance(consolidated_service_available, bool):
        raise ValueError("Service availability must be explicit Boolean flags.")
    plans = []
    for assignment in itertools.product(range(3), repeat=3):
        visited = sorted(set(assignment))
        if not all(service[store] for store in visited): continue
        if len(visited)>1 and not consolidated_service_available: continue
        if not all(stock[store,product] and eligible[store,product] and
                   (not substitute[store,product] or approved[store,product])
                   for product,store in enumerate(assignment)): continue
        goods = sum(int(PRICES_CENTS[store,product]) for product,store in enumerate(assignment))
        fees = int(SINGLE_STORE_FEES_CENTS[visited[0]]) if len(visited)==1 else PICKUP_PER_STORE_CENTS*len(visited)+CONSOLIDATED_COURIER_CENTS
        total = goods+fees
        if budget_cents is not None and total>=budget_cents: continue
        plans.append({"assignment": [STORES[store] for store in assignment], "product_ids": list(PRODUCTS),
                      "whole_pack_quantities": [1,1,1], "visited_stores": [STORES[store] for store in visited],
                      "goods_cents": goods, "fees_cents": fees, "total_cents": total})
    return sorted(plans,key=lambda p:(p["total_cents"],p["assignment"]))

def run():
    all_plans=enumerate_plans(budget_cents=None)
    single={p["visited_stores"][0]:p for p in all_plans if len(p["visited_stores"])==1}
    greedy_assignment=[STORES[int(np.argmin(PRICES_CENTS[:,product]))] for product in range(3)]
    greedy=next(p for p in all_plans if p["assignment"]==greedy_assignment)
    feasible=enumerate_plans(budget_cents=4000)
    return {"case_id":"V1C05-CASE02", "currency":"AUD", "money_unit":"integer cents",
            "data_status":"wholly synthetic assumed prices/fees/equivalence; not retailer quotes or service offers",
            "input_contract":"Three approved equivalent abstract lines P1/P2/P3, exactly one purchased pack each. Typed, voice and uploaded-list adapters are proposed, not implemented.",
            "stores":STORES,"products":PRODUCTS,"price_cents_store_by_product":PRICES_CENTS,
            "single_store_fees_cents":SINGLE_STORE_FEES_CENTS,
            "mixed_store_fee_formula":"200 cents per visited store + 800 cents hypothetical consolidated courier",
            "enumerated_assignment_count":len(all_plans),"all_assignments":all_plans,"single_store_plans":single,
            "greedy_item_price_plan":greedy,"strict_budget_cents":4000,"feasible_assignment_count":len(feasible),
            "minimum_total_plan":feasible[0] if feasible else None,
            "strict_budget_3300_feasible_count":len(enumerate_plans(budget_cents=3300)),
            "scope":"Exact finite allocation arithmetic only. No real stock, supplier/courier integration, ingredient/allergen checking, nutrition calculation, price forecast or purchase is performed."}

def main():
    result=plain(run());path=ROOT/"shopsmart_examples"/"basket_results.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))

if __name__=="__main__": main()
