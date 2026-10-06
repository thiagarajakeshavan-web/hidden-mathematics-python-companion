"""Additive synthetic ShopSmart worked-case contracts; no live integrations."""
from pathlib import Path
import importlib.util
import unittest
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def load(relative):
    spec=importlib.util.spec_from_file_location("basket_case",ROOT/relative)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

class V1C05BasketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lab=load("shopsmart_examples/basket_comparison.py");cls.result=cls.lab.run()

    def test_all_27_assignments_unique(self):
        rows=self.result["all_assignments"]
        self.assertEqual(len(rows),27)
        self.assertEqual(len({tuple(p["assignment"]) for p in rows}),27)
        self.assertTrue(all(p["whole_pack_quantities"]==[1,1,1] for p in rows))

    def test_single_store_whole_basket_fees(self):
        expected={"Coles":(2900,400,3300),"Woolworths":(2900,700,3600),"ALDI":(2500,900,3400)}
        for store,values in expected.items():
            row=self.result["single_store_plans"][store]
            self.assertEqual(tuple(row[k] for k in ("goods_cents","fees_cents","total_cents")),values)

    def test_greedy_merged_goods_and_all_fees(self):
        row=self.result["greedy_item_price_plan"]
        self.assertEqual(row["assignment"],["Coles","Woolworths","ALDI"])
        self.assertEqual((row["goods_cents"],row["fees_cents"],row["total_cents"]),(2100,1400,3500))

    def test_global_minimum_is_coles_only(self):
        row=self.result["minimum_total_plan"]
        self.assertEqual(row["assignment"],["Coles"]*3);self.assertEqual(row["total_cents"],3300)
        self.assertTrue(all(p["total_cents"]>=3300 for p in self.result["all_assignments"]))

    def test_strict_budget_excludes_equality(self):
        self.assertEqual(self.lab.enumerate_plans(budget_cents=3300),[])
        self.assertEqual(len(self.lab.enumerate_plans(budget_cents=3301)),1)
        self.assertTrue(all(p["total_cents"]<4000 for p in self.lab.enumerate_plans(budget_cents=4000)))

    def test_missing_stock_is_excluded(self):
        stock=np.ones((3,3),dtype=bool);stock[:,0]=False
        self.assertEqual(self.lab.enumerate_plans(stock=stock),[])
        stock=np.ones((3,3),dtype=bool);stock[0,0]=False
        rows=self.lab.enumerate_plans(stock=stock,budget_cents=None)
        self.assertTrue(all(p["assignment"][0]!="Coles" for p in rows));self.assertEqual(len(rows),18)

    def test_unavailable_store_service_is_excluded(self):
        rows=self.lab.enumerate_plans(store_service_available=np.array([False,True,True]),budget_cents=None)
        self.assertEqual(len(rows),8)
        self.assertTrue(all("Coles" not in p["visited_stores"] for p in rows))

    def test_missing_consolidation_excludes_mixed_plans(self):
        rows=self.lab.enumerate_plans(consolidated_service_available=False,budget_cents=None)
        self.assertEqual(len(rows),3);self.assertTrue(all(len(p["visited_stores"])==1 for p in rows))

    def test_ineligible_product_never_restored_by_cheap_price(self):
        eligible=np.ones((3,3),dtype=bool);eligible[2,2]=False
        rows=self.lab.enumerate_plans(product_eligible=eligible,budget_cents=None)
        self.assertTrue(all(p["assignment"][2]!="ALDI" for p in rows))

    def test_no_substitution_without_specific_approval(self):
        substitute=np.zeros((3,3),dtype=bool);substitute[0,0]=True
        rows=self.lab.enumerate_plans(requires_substitution=substitute,budget_cents=None)
        self.assertTrue(all(p["assignment"][0]!="Coles" for p in rows))
        approved=np.zeros((3,3),dtype=bool);approved[0,0]=True
        rows=self.lab.enumerate_plans(requires_substitution=substitute,approved_substitutions=approved,budget_cents=None)
        self.assertEqual(len(rows),27)

    def test_unknown_flags_and_noninteger_money_rejected(self):
        with self.assertRaises(ValueError): self.lab.enumerate_plans(stock=np.ones((3,3)))
        with self.assertRaises(ValueError): self.lab.enumerate_plans(stock=[[None]*3]*3)
        for budget in [33.,0,-1,True]:
            with self.assertRaises(ValueError): self.lab.enumerate_plans(budget_cents=budget)


class V1C10TimingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lab=load("shopsmart_examples/forecast_timing.py");cls.result=cls.lab.run()

    def test_ols_forecasts_from_past_only(self):
        r=self.result["ordinary_forecast"]
        self.assertTrue(np.all(np.asarray(r["training_days"])<=0))
        self.assertAlmostEqual(r["wash_intercept_cents"],1000)
        self.assertAlmostEqual(r["wash_slope_cents_per_day"],100/3)
        self.assertAlmostEqual(r["wash_forecast_cents"],1100)
        self.assertAlmostEqual(r["chocolate_slope_cents_per_day"],0)
        self.assertAlmostEqual(r["chocolate_forecast_cents"],600)

    def test_all_state_prices_include_goods_and_delivery(self):
        r=self.result["delay_cost_200"]
        self.assertEqual(r["today_delivered_cents"],1000+600+1100+600)
        self.assertEqual(r["promotion_future_delivered_cents"],600+300+1100+600)
        self.assertEqual(r["ordinary_future_delivered_cents"],1100+600+1100+600)

    def test_expected_cost_and_wait_decision(self):
        r=self.result["delay_cost_200"]
        self.assertEqual(r["expected_future_delivered_cents"],2920)
        self.assertEqual(r["expected_wait_cost_with_delay_cents"],3120)
        self.assertEqual(r["expected_saving_vs_today_cents"],180)
        self.assertEqual(r["synthetic_decision"],"wait")

    def test_larger_delay_cost_reverses_decision(self):
        r=self.result["delay_cost_400"]
        self.assertEqual(r["expected_wait_cost_with_delay_cents"],3320)
        self.assertEqual(r["expected_saving_vs_today_cents"],-20)
        self.assertEqual(r["synthetic_decision"],"buy_now")

    def test_deadline_is_hard_feasibility_constraint(self):
        r=self.result["need_before_day3"]
        self.assertFalse(r["waiting_feasible"]);self.assertEqual(r["synthetic_decision"],"buy_now")
        self.assertTrue(self.lab.compare_timing(need_by_day=3)["waiting_feasible"])

    def test_stock_eligibility_or_service_cannot_be_traded_for_savings(self):
        for flag in ("waiting_stock_available","waiting_eligible","waiting_service_available"):
            r=self.lab.compare_timing(**{flag:False})
            self.assertFalse(r["waiting_feasible"]);self.assertEqual(r["synthetic_decision"],"buy_now")

    def test_expected_cost_endpoints_and_tie_rule(self):
        self.assertEqual(self.lab.compare_timing(promotion_probability=0)["expected_future_delivered_cents"],3400)
        self.assertEqual(self.lab.compare_timing(promotion_probability=1)["expected_future_delivered_cents"],2600)
        self.assertEqual(self.lab.compare_timing(delay_cost_cents=380)["synthetic_decision"],"buy_now")

    def test_invalid_probability_money_deadline_and_unknown_flags(self):
        for probability in [-.1,1.1,"nan","inf"]:
            with self.assertRaises(ValueError): self.lab.compare_timing(promotion_probability=probability)
        for kwargs in ({"delay_cost_cents":-1},{"delay_cost_cents":2.5},{"need_by_day":-1},{"need_by_day":float("nan")},{"waiting_eligible":None}):
            with self.assertRaises(ValueError): self.lab.compare_timing(**kwargs)

if __name__=="__main__": unittest.main()
