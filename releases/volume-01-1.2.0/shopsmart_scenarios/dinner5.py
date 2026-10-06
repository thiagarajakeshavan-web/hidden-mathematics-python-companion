"""V1C05-CASE04: vegan dinner-for-five whole-pack synthetic budget gate.

No real ingredient labels, suppliers or kitchens are verified by this module.
The fail-closed teaching gate cannot certify a food as safe for an allergy.
"""
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shopsmart_scenarios.grocery30 import HERE, integer

TREE_NUTS = ("almond", "Brazil nut", "cashew", "hazelnut", "macadamia", "pecan", "pistachio", "pine nut", "walnut")
ALLERGENS = ("peanut",) + TREE_NUTS
VERIFIED_LENTIL_NUTRIENTS = {"protein_g": "7.3", "dietary_fibre_g": "4.1", "iron_mg": "1.63", "folate_ug": "14"}
VERIFIED_LENTIL_URL = "https://www.foodstandards.gov.au/science-data/food-nutrient-databases/afcd/search/food/F005177"
FEE_FIELDS = {"delivery_cents", "handling_cents", "other_mandatory_cents"}


def load_fixture():
    return json.loads((HERE / "data" / "dinner5.json").read_text(encoding="utf-8"))


def candidate_reasons(item, profile):
    reasons = []
    if profile["vegan_required"] is not True:
        raise ValueError("This case models a strictly vegan meal, not vegetarian eligibility.")
    exclusions = profile["excluded_allergens"]
    if not isinstance(exclusions, list) or not exclusions or len(set(exclusions)) != len(exclusions) or any(a not in ALLERGENS for a in exclusions):
        raise ValueError("Declare a unique explicit list of supported allergens; 'nut-free' is ambiguous.")
    if item.get("vegan_status") != "ACCEPTABLE_IN_FIXTURE":
        reasons.append("vegan_status_not_acceptable")
    if item.get("ingredient_evidence_current") is not True:
        reasons.append("ingredient_evidence_stale_or_unknown")
    for allergen in exclusions:
        record = item.get("allergen_evidence", {}).get(allergen, {})
        if record.get("ingredient_status") != "ABSENT_IN_FIXTURE":
            reasons.append(f"{allergen}:ingredient_present_or_unknown")
        if record.get("cross_contact_status") != "REVIEWED_ACCEPTABLE_IN_FIXTURE":
            reasons.append(f"{allergen}:cross_contact_unresolved")
        if record.get("label_current") is not True:
            reasons.append(f"{allergen}:label_stale_or_unknown")
    return reasons


def positive_decimal(value, name, allow_zero=False):
    if isinstance(value, bool):
        raise ValueError(f"{name} must not be Boolean.")
    try:
        result = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"Invalid {name}.") from None
    if not result.is_finite() or result < 0 or (result == 0 and not allow_zero):
        raise ValueError(f"{name} must be finite and {'nonnegative' if allow_zero else 'positive'}.")
    return result


def lentil_nutrition(source, servings):
    integer(servings, "servings", 1)
    if source["source_food_key"] != "F005177":
        raise ValueError("This example is verified only against the stated cooked, drained lentil record.")
    if source["source_url"] != VERIFIED_LENTIL_URL or source["per_100g"] != VERIFIED_LENTIL_NUTRIENTS:
        raise ValueError("Nutrient names, units, values and source URL must match the verified reference fixture; new references need separate verification.")
    mass = positive_decimal(source["assumed_measured_cooked_drained_mass_g"], "cooked lentil mass")
    batch, per_portion = {}, {}
    for nutrient, value in source["per_100g"].items():
        amount = positive_decimal(value, nutrient, allow_zero=True) * mass / 100
        batch[nutrient] = format(amount, "f")
        per_portion[nutrient] = format(amount / servings, "f")
    return {"scope": "Lentil component only; not whole-meal totals or an adequacy judgment.",
            "source_url": source["source_url"], "source_food_key": source["source_food_key"],
            "assumed_cooked_drained_mass_g": format(mass, "f"), "servings": servings,
            "lentil_batch_contribution": batch, "lentil_contribution_per_serving": per_portion,
            "whole_meal_nutrient_totals": None,
            "assumption": "Use the cooked drained weight, not the purchased dry weight. Weigh the actual cooked batch; change this input if its mass differs. Reference values and assumed mass do not verify a real product or recipe."}


def solve_kit(fixture=None, *, profile_name="peanut_and_named_tree_nuts", strict_budget_cents=None):
    fixture = load_fixture() if fixture is None else deepcopy(fixture)
    integer(fixture["servings"], "servings", 1)
    budget = fixture["strict_budget_cents"] if strict_budget_cents is None else strict_budget_cents
    integer(budget, "strict budget", 1)
    integer(fixture["minimum_order_cents"], "minimum order")
    if fixture["minimum_order_cents"] != 0 or fixture["membership_required"] is not False:
        raise ValueError("Unsupported minimum-order or membership rule.")
    if set(fixture["fees"]) != FEE_FIELDS:
        raise ValueError("Declare delivery, handling and other mandatory fees explicitly, including zero when free.")
    for fee in fixture["fees"].values():
        integer(fee, "fee")
    profile = fixture["profiles"][profile_name]
    if not fixture["items"]:
        raise ValueError("A complete recipe needs ingredient lines.")
    lines, exclusions, seen = [], [], set()
    recipe_cost = Fraction(0)
    for item in fixture["items"]:
        if not item["item_id"] or item["item_id"] in seen:
            raise ValueError("Ingredient IDs must be unique and nonempty.")
        seen.add(item["item_id"])
        for field in ("recipe_quantity", "pack_quantity"):
            integer(item[field], field, 1)
        integer(item["price_per_pack_cents"], "pack price")
        if item["stock_packs"] is not None:
            integer(item["stock_packs"], "stock packs")
        if item["unit"] not in ("g", "ml", "count"):
            raise ValueError("Unsupported recipe unit.")
        packs = (item["recipe_quantity"] + item["pack_quantity"] - 1) // item["pack_quantity"]
        reasons = candidate_reasons(item, profile)
        if item["stock_packs"] is None or item["stock_packs"] < packs:
            reasons.append("insufficient_or_unknown_stock")
        if reasons:
            exclusions.append({"item_id": item["item_id"], "reasons": reasons})
        goods = packs * item["price_per_pack_cents"]
        prorated = Fraction(item["recipe_quantity"] * item["price_per_pack_cents"], item["pack_quantity"])
        recipe_cost += prorated
        lines.append({"item_id": item["item_id"], "ingredient": item["ingredient"], "unit": item["unit"],
                      "recipe_quantity": item["recipe_quantity"], "pack_quantity": item["pack_quantity"],
                      "packs_to_purchase": packs, "purchased_quantity": packs * item["pack_quantity"],
                      "leftover_quantity": packs * item["pack_quantity"] - item["recipe_quantity"],
                      "whole_purchase_cents": goods,
                      "prorated_recipe_cost_cents": {"numerator": prorated.numerator, "denominator": prorated.denominator},
                      "synthetic_eligibility": "PASS_FIXTURE" if not reasons else "EXCLUDED"})
    goods = sum(line["whole_purchase_cents"] for line in lines)
    fees = sum(fixture["fees"].values())
    payable = goods + fees
    kitchen_ok = fixture["kitchen_cross_contact_reviewed_in_fixture"] is True
    complete = not exclusions and kitchen_ok
    feasible = complete and payable < budget
    return {"case_id": "V1C05-CASE04", "meal": fixture["meal"], "servings": fixture["servings"],
            "profile": profile_name, "excluded_allergens": profile["excluded_allergens"],
            "status": "SYNTHETIC_FEASIBLE" if feasible else "INFEASIBLE",
            "complete_kit_eligible_in_fixture": complete, "under_strict_budget": payable < budget,
            "strict_budget_cents": budget, "whole_purchase_goods_cents": goods,
            "fees": fixture["fees"], "fees_cents": fees, "payable_cents": payable,
            "budget_headroom_cents": budget - payable,
            "prorated_recipe_ingredient_cost_cents": {"numerator": recipe_cost.numerator,
                                                       "denominator": recipe_cost.denominator,
                                                       "decimal": float(recipe_cost)},
            "prorated_cost_note": "An accounting allocation of used ingredients, excluding fees; not a purchasable basket total.",
            "purchased_pack_count": sum(line["packs_to_purchase"] for line in lines),
            "exclusions": exclusions, "kitchen_review_passes_fixture": kitchen_ok,
            "lines": lines, "pantry_assumptions": fixture["pantry_assumptions"],
            "recipe_steps": fixture["recipe_steps"],
            "nutrition": lentil_nutrition(fixture["nutrition_input"], fixture["servings"]),
            "actual_product_clearance": False,
            "real_world_status": "WITHHOLD_ALLERGY_COMPLIANT_RECOMMENDATION_PENDING_CURRENT_PRODUCT_LABELS_CROSS_CONTACT_AND_APPROPRIATE_HUMAN_REVIEW",
            "scope": "One home-cooked vegan dinner for five, not five days, a restaurant order or a clinically balanced meal plan. All commercial and eligibility inputs are fiction. Peanut and named tree nuts are separate constraints; the phrase nut-free alone is insufficient. UNKNOWN, stale, ambiguous, conflicting or missing relevant evidence is excluded. Cost cannot override a dietary or allergen gate."}


def run():
    result = solve_kit()
    result["currency"] = "AUD"
    result["data_status"] = load_fixture()["data_status"]
    return result


def main():
    result = run()
    (HERE / "dinner5_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"case": result["case_id"], "payable_cents": result["payable_cents"], "servings": result["servings"], "status": result["status"]}))


if __name__ == "__main__":
    main()
