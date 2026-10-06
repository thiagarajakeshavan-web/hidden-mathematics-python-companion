"""New independent regression, brute-force oracle, uncertainty and safety-gate tests."""
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shopsmart_scenarios import dinner5, grocery30, timing30
spec = importlib.util.spec_from_file_location("map_mle", ROOT / "V1C04" / "CASE02" / "map_mle.py")
map_mle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(map_mle)
spec_nfl = importlib.util.spec_from_file_location("no_free_lunch", ROOT / "V1C07" / "CASE02" / "no_free_lunch.py")
no_free_lunch = importlib.util.module_from_spec(spec_nfl)
spec_nfl.loader.exec_module(no_free_lunch)


class GroceryTests(unittest.TestCase):
    def test_unknown_csv_cold_chain_is_not_false(self):
        text = (grocery30.HERE / "data" / "grocery30.csv").read_text()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.csv"
            path.write_text(text.replace(",true", ",UNKNOWN", 1))
            with self.assertRaises(ValueError):
                grocery30.load_catalogue(path)

    def test_exactly_30_unique_lines(self):
        rows = grocery30.load_catalogue()
        self.assertEqual(len(rows), 30)
        self.assertEqual(len({r["item_id"] for r in rows}), 30)

    def test_seven_subsets_all_checked(self):
        answer = grocery30.solve()
        self.assertEqual([e["store_mask"] for e in answer["subsets"]], list(range(1, 8)))
        self.assertTrue(all(e["feasible"] for e in answer["subsets"]))
        self.assertEqual([e["plan"]["payable_cents"] for e in answer["subsets"]],
                         [11630, 11370, 11390, 10920, 11210, 11030, 11100])

    def test_whole_pack_rounding_and_surplus(self):
        rows = grocery30.load_catalogue()
        pasta = grocery30.line_option(rows[1], 0)
        self.assertEqual((pasta["packs"], pasta["purchased_quantity"], pasta["surplus_quantity"]), (2, 1000, 250))
        self.assertEqual(grocery30.line_option(rows[1], 2)["packs"], 1)
        self.assertEqual(grocery30.line_option(rows[28], 0)["packs"], 2)
        self.assertEqual(grocery30.line_option(rows[28], 2)["packs"], 1)

    def test_single_store_beats_merge_after_fees(self):
        result = grocery30.run()
        self.assertEqual(result["optimization"]["best_plan"]["stores"], ["ALDI"])
        self.assertEqual(result["savings_vs_cheapest_single_cents"], 0)
        three = result["optimization"]["subsets"][-1]["plan"]
        self.assertLess(three["goods_cents"], result["single_store_plans"]["ALDI"]["goods_cents"])
        self.assertGreater(three["payable_cents"], result["single_store_plans"]["ALDI"]["payable_cents"])

    def test_fixed_split_is_not_forced_optimum(self):
        result = grocery30.run()
        fixed = result["fixed_10_10_10_plan"]
        self.assertEqual(fixed["line_counts"], {"Coles": 10, "Woolworths": 10, "ALDI": 10})
        self.assertEqual(fixed["payable_cents"], 11570)
        self.assertEqual(result["optimization"]["subsets"][-1]["plan"]["line_counts"], {"Coles": 8, "Woolworths": 11, "ALDI": 11})

    def test_lower_consolidation_fee_changes_decision(self):
        routes = grocery30.default_routes()
        for mask, route in routes.items():
            if mask.bit_count() > 1:
                route["delivery_cents"] = 500
        best = grocery30.solve(routes=routes)["best_plan"]
        self.assertEqual(best["payable_cents"], 10730)
        self.assertEqual(best["stores"], ["Woolworths", "ALDI"])

    def test_dp_matches_exhaustive_oracle_for_small_inputs(self):
        rng = random.Random(12026)
        for trial in range(12):
            rows = deepcopy(grocery30.load_catalogue()[:5])
            for row in rows:
                for offer in row["offers"]:
                    offer["price_cents"] = rng.randrange(50, 501)
                    offer["stock_packs"] = rng.choice([0, 5, 5])
            routes = grocery30.default_routes()
            actual = grocery30.solve(rows, routes)
            for entry in actual["subsets"]:
                all_plans = [grocery30.make_plan(rows, list(a), routes) for a in itertools.product(range(3), repeat=5)
                             if sum(1 << s for s in set(a)) == entry["store_mask"]]
                feasible = [p for p in all_plans if p is not None]
                expected = min((p["payable_cents"] for p in feasible), default=None)
                got = entry["plan"]["payable_cents"] if entry["plan"] else None
                self.assertEqual(got, expected, (trial, entry["store_mask"]))

    def test_transition_bound_avoids_three_power_30(self):
        answer = grocery30.solve()
        self.assertLessEqual(answer["dp_transitions"], 30 * 3 * 8)
        self.assertEqual(answer["naive_assignment_count_avoided"], 205891132094649)

    def test_missing_stock_does_not_rank_partial_basket(self):
        rows = grocery30.load_catalogue()
        rows[13]["offers"][2]["stock_packs"] = 0
        entry = grocery30.solve(rows)["subsets"][3]
        self.assertFalse(entry["feasible"])
        self.assertIsNone(entry["plan"])
        self.assertEqual(entry["missing_item_ids"], ["G14"])

    def test_unknown_price_stock_equivalence_fail_closed(self):
        for field in ("price_cents", "stock_packs", "equivalence_approved"):
            rows = grocery30.load_catalogue()
            rows[0]["offers"][0][field] = None
            self.assertFalse(grocery30.solve(rows)["subsets"][0]["feasible"])

    def test_all_stores_missing_a_line_is_infeasible(self):
        rows = grocery30.load_catalogue()
        for offer in rows[0]["offers"]:
            offer["stock_packs"] = 0
        self.assertIsNone(grocery30.solve(rows)["best_plan"])

    def test_unknown_service_window_and_cold_chain_excluded(self):
        for key in grocery30.ROUTE_CHECKS:
            routes = grocery30.default_routes()
            routes[4][key] = None
            self.assertFalse(grocery30.solve(routes=routes)["subsets"][3]["feasible"])

    def test_strict_budget_boundary(self):
        self.assertIsNone(grocery30.solve(strict_budget_cents=10920)["best_plan"])
        self.assertEqual(grocery30.solve(strict_budget_cents=10921)["best_plan"]["payable_cents"], 10920)

    def test_invalid_numeric_and_unsupported_fee_rules_rejected(self):
        for value in (True, -1, 2.5):
            rows = grocery30.load_catalogue()
            rows[0]["offers"][0]["price_cents"] = value
            with self.assertRaises(ValueError):
                grocery30.solve(rows)
        for field, value in (("minimum_spend_cents", 1000), ("membership_required", True)):
            routes = grocery30.default_routes()
            routes[1][field] = value
            with self.assertRaises(ValueError):
                grocery30.solve(routes=routes)

    def test_duplicate_item_and_invalid_pack_rejected(self):
        rows = grocery30.load_catalogue()
        rows[1]["item_id"] = rows[0]["item_id"]
        with self.assertRaises(ValueError):
            grocery30.solve(rows)
        rows = grocery30.load_catalogue()
        rows[0]["offers"][0]["pack"] = 0
        with self.assertRaises(ValueError):
            grocery30.solve(rows)

    def test_snapshot_and_no_input_mutation(self):
        rows, routes = grocery30.load_catalogue(), grocery30.default_routes()
        before = deepcopy((rows, routes))
        grocery30.solve(rows, routes)
        self.assertEqual((rows, routes), before)
        self.assertEqual(grocery30.run(), json.loads((grocery30.HERE / "grocery30_results.json").read_text()))


class TimingTests(unittest.TestCase):
    def test_forecast_horizons_follow_custom_days(self):
        spec = timing30.load_scenarios()
        spec["future_days"][0]["day"] = 4
        self.assertEqual(timing30.run(scenarios=spec)["forecast_horizons_days"], [3, 4])

    def test_exact_expected_costs_and_decisions(self):
        result = timing30.run()
        self.assertEqual([d["expected_decision_cost_cents"]["decimal"] for d in result["days"]], [10920, 10910, 10588])
        self.assertEqual((result["risk_neutral_selected_day"], result["minimax_selected_day"]), (3, 0))
        self.assertEqual([d["waiting_cost_cents"] for d in result["days"]], [0, 300, 450])
        self.assertEqual(result["days"][2]["net_expected_saving_vs_today_cents"]["decimal"], 332)

    def test_due_today_forbids_waiting(self):
        self.assertEqual(timing30.run(need_by_day=0)["risk_neutral_selected_day"], 0)

    def test_due_day_two_forbids_day_three(self):
        self.assertEqual(timing30.run(need_by_day=2)["risk_neutral_selected_day"], 2)

    def test_high_waiting_cost_can_favour_today(self):
        self.assertEqual(timing30.run(waiting_cost_per_day_cents=1000)["risk_neutral_selected_day"], 0)

    def test_promotion_overrides_forecast_only_in_valid_window(self):
        spec = timing30.load_scenarios()
        state = spec["future_days"][0]["states"][0]
        rows, applied = timing30.scenario_rows(grocery30.load_catalogue(), 2, state, spec["promotions"])
        self.assertEqual(rows[27]["offers"][0]["price_cents"], 700)
        self.assertEqual(rows[0]["offers"][0]["price_cents"], 260)
        self.assertEqual(len(applied), 2)
        future, applied = timing30.scenario_rows(grocery30.load_catalogue(), 4, state, spec["promotions"])
        self.assertEqual(future[27]["offers"][0]["price_cents"], 1120)
        self.assertEqual(applied, [])

    def test_day_two_aldi_only_is_infeasible(self):
        for state in timing30.run()["days"][1]["states"]:
            entry = state["optimization"]["subsets"][3]
            self.assertFalse(entry["feasible"])
            self.assertEqual(entry["missing_item_ids"], ["G14"])

    def test_infeasible_scenario_not_averaged_away(self):
        spec = timing30.load_scenarios()
        spec["future_days"][0]["states"][0]["stock_overrides"] = [
            {"item_id": "G01", "store": name, "stock_packs": 0} for name in grocery30.STORES]
        day = timing30.run(scenarios=spec)["days"][1]
        self.assertIsNone(day["expected_decision_cost_cents"])
        self.assertEqual(day["infeasible_probability_basis_points"], 2000)

    def test_invalid_probabilities_and_live_claim_rejected(self):
        spec = timing30.load_scenarios()
        spec["future_days"][0]["states"][0]["probability_basis_points"] = 1000
        with self.assertRaises(ValueError):
            timing30.run(scenarios=spec)
        spec = timing30.load_scenarios()
        spec["promotions"][0]["evidence_status"] = "REAL_CONFIRMED"
        with self.assertRaises(ValueError):
            timing30.run(scenarios=spec)

    def test_negative_wait_cost_rejected(self):
        with self.assertRaises(ValueError):
            timing30.run(waiting_cost_per_day_cents=-1)

    def test_saved_timing_results_match(self):
        self.assertEqual(timing30.run(), json.loads((grocery30.HERE / "timing30_results.json").read_text()))


class DinnerTests(unittest.TestCase):
    def test_missing_fee_fields_are_not_free_delivery(self):
        for fees in ({}, {"delivery_cents": 0}):
            fixture = dinner5.load_fixture()
            fixture["fees"] = fees
            with self.assertRaises(ValueError):
                dinner5.solve_kit(fixture)

    def test_nutrient_reference_edits_require_reverification(self):
        for mutation in ("unit", "value", "url"):
            source = dinner5.load_fixture()["nutrition_input"]
            if mutation == "unit":
                source["per_100g"]["protein_mg"] = source["per_100g"].pop("protein_g")
            elif mutation == "value":
                source["per_100g"]["protein_g"] = "100"
            else:
                source["source_url"] = "https://example.com/unverified"
            with self.assertRaises(ValueError):
                dinner5.lentil_nutrition(source, 5)

    def test_boolean_nutrient_mass_and_minimum_order_rejected(self):
        source = dinner5.load_fixture()["nutrition_input"]
        source["assumed_measured_cooked_drained_mass_g"] = True
        with self.assertRaises(ValueError):
            dinner5.lentil_nutrition(source, 5)
        fixture = dinner5.load_fixture()
        fixture["minimum_order_cents"] = False
        with self.assertRaises(ValueError):
            dinner5.solve_kit(fixture)

    def test_five_people_one_dinner_complete_basket(self):
        result = dinner5.run()
        self.assertEqual(result["servings"], 5)
        self.assertEqual(result["status"], "SYNTHETIC_FEASIBLE")
        self.assertEqual((len(result["lines"]), result["purchased_pack_count"]), (13, 14))
        self.assertEqual((result["whole_purchase_goods_cents"], result["fees_cents"], result["payable_cents"]), (2680, 600, 3280))
        self.assertEqual(result["budget_headroom_cents"], 720)

    def test_strict_under_40_not_less_equal(self):
        self.assertEqual(dinner5.solve_kit(strict_budget_cents=3280)["status"], "INFEASIBLE")
        self.assertEqual(dinner5.solve_kit(strict_budget_cents=3281)["status"], "SYNTHETIC_FEASIBLE")

    def test_complete_whole_packs_differ_from_prorated_recipe(self):
        result = dinner5.run()
        self.assertLess(result["prorated_recipe_ingredient_cost_cents"]["decimal"], result["whole_purchase_goods_cents"])
        self.assertEqual(result["lines"][0]["leftover_quantity"], 650)
        self.assertEqual(result["lines"][2]["packs_to_purchase"], 2)
        self.assertEqual(result["lines"][9]["purchased_quantity"], 500)

    def test_fees_cannot_be_omitted_from_budget(self):
        fixture = dinner5.load_fixture()
        fixture["fees"]["delivery_cents"] = 1300
        result = dinner5.solve_kit(fixture)
        self.assertEqual(result["payable_cents"], 4080)
        self.assertEqual(result["status"], "INFEASIBLE")

    def test_every_food_ingredient_included_no_pantry_oil_or_spice(self):
        names = {i["ingredient"] for i in dinner5.load_fixture()["items"]}
        self.assertTrue({"Cooking oil", "Ground cumin", "Paprika", "Black pepper"} <= names)
        self.assertIn("Drinking water only", dinner5.run()["pantry_assumptions"][0])

    def test_nonvegan_excluded_even_if_cheaper(self):
        fixture = dinner5.load_fixture()
        fixture["items"][0]["vegan_status"] = "CONTAINS_ANIMAL_PRODUCT"
        fixture["items"][0]["price_per_pack_cents"] = 1
        self.assertEqual(dinner5.solve_kit(fixture)["status"], "INFEASIBLE")

    def test_unknown_vegan_excluded(self):
        fixture = dinner5.load_fixture()
        fixture["items"][0]["vegan_status"] = "UNKNOWN"
        self.assertFalse(dinner5.solve_kit(fixture)["complete_kit_eligible_in_fixture"])

    def test_peanut_and_tree_nuts_are_distinct_constraints(self):
        fixture = dinner5.load_fixture()
        fixture["items"][0]["allergen_evidence"]["cashew"]["ingredient_status"] = "CONTAINS"
        self.assertEqual(dinner5.solve_kit(fixture, profile_name="peanut_only")["status"], "SYNTHETIC_FEASIBLE")
        self.assertEqual(dinner5.solve_kit(fixture, profile_name="peanut_and_named_tree_nuts")["status"], "INFEASIBLE")
        self.assertFalse(dinner5.solve_kit(fixture, profile_name="peanut_only")["actual_product_clearance"])

    def test_unknown_missing_stale_or_conflicting_allergen_evidence_excluded(self):
        for mutation in ("unknown", "missing", "stale", "cross_contact", "conflicting"):
            fixture = dinner5.load_fixture()
            record = fixture["items"][0]["allergen_evidence"]["peanut"]
            if mutation == "unknown": record["ingredient_status"] = "UNKNOWN"
            elif mutation == "missing": del fixture["items"][0]["allergen_evidence"]["peanut"]
            elif mutation == "stale": record["label_current"] = False
            elif mutation == "cross_contact": record["cross_contact_status"] = "MAY_CONTAIN"
            else: record["ingredient_status"] = "CONFLICTING"
            self.assertEqual(dinner5.solve_kit(fixture)["status"], "INFEASIBLE", mutation)

    def test_absence_of_declared_allergen_alone_is_insufficient(self):
        fixture = dinner5.load_fixture()
        del fixture["items"][0]["allergen_evidence"]["peanut"]["cross_contact_status"]
        self.assertEqual(dinner5.solve_kit(fixture)["status"], "INFEASIBLE")

    def test_kitchen_cross_contact_unknown_blocks(self):
        fixture = dinner5.load_fixture()
        fixture["kitchen_cross_contact_reviewed_in_fixture"] = None
        self.assertEqual(dinner5.solve_kit(fixture)["status"], "INFEASIBLE")

    def test_missing_ingredient_stock_blocks_complete_kit(self):
        for stock in (0, None):
            fixture = dinner5.load_fixture()
            fixture["items"][2]["stock_packs"] = stock
            self.assertEqual(dinner5.solve_kit(fixture)["status"], "INFEASIBLE")

    def test_nut_free_label_is_rejected_as_ambiguous(self):
        fixture = dinner5.load_fixture()
        fixture["profiles"]["peanut_and_named_tree_nuts"]["excluded_allergens"] = ["nut-free"]
        with self.assertRaises(ValueError):
            dinner5.solve_kit(fixture)

    def test_verified_lentil_nutrients_scaled_by_cooked_mass_and_five(self):
        result = dinner5.run()["nutrition"]
        self.assertEqual(result["lentil_batch_contribution"], {"protein_g": "73.0", "dietary_fibre_g": "41.0", "iron_mg": "16.30", "folate_ug": "140"})
        self.assertEqual(result["lentil_contribution_per_serving"], {"protein_g": "14.6", "dietary_fibre_g": "8.2", "iron_mg": "3.26", "folate_ug": "28"})
        self.assertIsNone(result["whole_meal_nutrient_totals"])

    def test_cooked_mass_changes_nutrients_not_dry_purchase(self):
        source = dinner5.load_fixture()["nutrition_input"]
        source["assumed_measured_cooked_drained_mass_g"] = "800"
        result = dinner5.lentil_nutrition(source, 5)
        self.assertEqual(Decimal(result["lentil_contribution_per_serving"]["protein_g"]), Decimal("11.68"))
        self.assertEqual(source["dry_pack_purchase_g"], 500)

    def test_invalid_nutrient_mass_and_servings_rejected(self):
        for value in ("NaN", "Infinity", "-1", "0"):
            source = dinner5.load_fixture()["nutrition_input"]
            source["assumed_measured_cooked_drained_mass_g"] = value
            with self.assertRaises(ValueError):
                dinner5.lentil_nutrition(source, 5)
        with self.assertRaises(ValueError):
            dinner5.lentil_nutrition(dinner5.load_fixture()["nutrition_input"], 0)

    def test_unknown_real_products_remain_uncleared(self):
        result = dinner5.run()
        self.assertFalse(result["actual_product_clearance"])
        self.assertTrue(result["real_world_status"].startswith("WITHHOLD"))

    def test_snapshot_and_no_input_mutation(self):
        fixture = dinner5.load_fixture()
        before = deepcopy(fixture)
        dinner5.solve_kit(fixture)
        self.assertEqual(fixture, before)
        self.assertEqual(dinner5.run(), json.loads((grocery30.HERE / "dinner5_results.json").read_text()))


class MapMleTests(unittest.TestCase):
    def test_exact_mle_map_mean_and_posterior(self):
        result = map_mle.estimate()
        self.assertEqual((result["posterior_alpha"], result["posterior_beta"]), (9, 5))
        self.assertEqual((result["mle"], result["map"], result["posterior_mean"]), (Fraction(7, 10), Fraction(2, 3), Fraction(9, 14)))

    def test_uniform_prior_map_equals_mle(self):
        result = map_mle.estimate(prior_alpha=1, prior_beta=1)
        self.assertEqual(result["map"], result["mle"])

    def test_boundary_mode_not_misusing_interior_formula(self):
        with self.assertRaises(ValueError):
            map_mle.estimate(successes=0, trials=10, prior_alpha=1, prior_beta=1)

    def test_invalid_counts_and_prior(self):
        for args in ({"trials": 0}, {"successes": 11}, {"successes": True}, {"prior_alpha": 0}):
            with self.assertRaises(ValueError):
                map_mle.estimate(**args)

    def test_map_results_snapshot(self):
        self.assertEqual(map_mle.run(), json.loads((ROOT / "V1C04" / "CASE02" / "results.json").read_text()))


class NoFreeLunchTests(unittest.TestCase):
    def test_exact_consistent_targets(self):
        self.assertEqual(no_free_lunch.consistent_targets(), [(0, 0), (0, 1)])
        self.assertEqual(no_free_lunch.consistent_targets(1), [(1, 0), (1, 1)])

    def test_deterministic_and_randomized_errors_equal_half(self):
        for label in (0, 1):
            self.assertEqual(no_free_lunch.mean_unseen_error(label), Fraction(1, 2))
        for q in (0, Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), 1):
            self.assertEqual(no_free_lunch.randomized_unseen_error(q), Fraction(1, 2))

    def test_invalid_labels_and_probabilities_rejected(self):
        for value in (True, 2, -1):
            with self.assertRaises(ValueError):
                no_free_lunch.consistent_targets(value)
            with self.assertRaises(ValueError):
                no_free_lunch.mean_unseen_error(value)
        for q in (True, 0.5, -1, Fraction(3, 2)):
            with self.assertRaises(ValueError):
                no_free_lunch.randomized_unseen_error(q)

    def test_saved_nfl_results_match(self):
        self.assertEqual(no_free_lunch.run(), json.loads((ROOT / "V1C07" / "CASE02" / "results.json").read_text()))


if __name__ == "__main__":
    unittest.main()
