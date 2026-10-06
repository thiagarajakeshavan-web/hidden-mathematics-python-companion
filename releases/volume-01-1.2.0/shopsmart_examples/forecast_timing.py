"""V1C10-CASE02: a synthetic trend forecast and a separate wait-cost decision.

No real retailer/SKU history, confirmed promotion or trained promotion model.
No price retrieval, speech/OCR, health check, order or courier integration.
"""
from pathlib import Path
from fractions import Fraction
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.linear_model import LinearRegression
from common import ROOT, plain

DAYS = np.array([-6., -3., 0.])
WASH_PRICES_CENTS = np.array([800, 900, 1000])
CHOC_PRICES_CENTS = np.array([600, 600, 600])
OTHER_GOODS_CENTS = 1100
DELIVERY_CENTS = 600
TODAY_CENTS = 3300
PROMOTION_DAY3_CENTS = 2600
FORECAST_DAY = 3

def ordinary_forecast():
    """OLS uses only observations at or before today's origin t=0."""
    x = DAYS.reshape(-1,1)
    wash=LinearRegression().fit(x,WASH_PRICES_CENTS)
    chocolate=LinearRegression().fit(x,CHOC_PRICES_CENTS)
    wash_forecast=float(wash.predict([[FORECAST_DAY]])[0])
    chocolate_forecast=float(chocolate.predict([[FORECAST_DAY]])[0])
    # State costs are rounded to the nearest cent after this illustrative fit.
    total=round(wash_forecast)+round(chocolate_forecast)+OTHER_GOODS_CENTS+DELIVERY_CENTS
    return {"training_days":DAYS,"wash_history_cents":WASH_PRICES_CENTS,"chocolate_history_cents":CHOC_PRICES_CENTS,
            "wash_intercept_cents":float(wash.intercept_),"wash_slope_cents_per_day":float(wash.coef_[0]),
            "chocolate_intercept_cents":float(chocolate.intercept_),"chocolate_slope_cents_per_day":float(chocolate.coef_[0]),
            "forecast_day":FORECAST_DAY,"wash_forecast_cents":wash_forecast,"chocolate_forecast_cents":chocolate_forecast,
            "ordinary_future_total_cents":total,
            "note":"Three constructed observations fit a line but cannot validate real forecasting. No future observation is used. The promotion probability and promotion prices come from separate assumptions, not this regression."}

def compare_timing(*, promotion_probability="0.6", delay_cost_cents=200, need_by_day=3,
                   waiting_stock_available=True, waiting_eligible=True, waiting_service_available=True):
    try: probability=Fraction(str(promotion_probability))
    except (ValueError,ZeroDivisionError) as exc: raise ValueError("Use a finite promotion probability in [0,1].") from exc
    if not 0<=probability<=1: raise ValueError("Promotion probability must lie in [0,1].")
    if not isinstance(delay_cost_cents,int) or isinstance(delay_cost_cents,bool) or delay_cost_cents<0:
        raise ValueError("Delay cost must be a nonnegative integer number of cents.")
    if not isinstance(need_by_day,(int,float)) or isinstance(need_by_day,bool) or not np.isfinite(need_by_day) or need_by_day<0:
        raise ValueError("Need-by day must be a finite nonnegative number relative to today.")
    flags=[waiting_stock_available,waiting_eligible,waiting_service_available]
    if not all(isinstance(flag,bool) for flag in flags): raise ValueError("Availability and eligibility require explicit Boolean flags.")
    ordinary=ordinary_forecast()["ordinary_future_total_cents"]
    expected=probability*PROMOTION_DAY3_CENTS+(1-probability)*ordinary
    adjusted=expected+delay_cost_cents
    reasons=[]
    if need_by_day<FORECAST_DAY: reasons.append("forecast day is after the need-by deadline")
    if not waiting_stock_available: reasons.append("future stock is not assumed available")
    if not waiting_eligible: reasons.append("future product eligibility is not established")
    if not waiting_service_available: reasons.append("future delivery service is not assumed available")
    feasible=not reasons
    decision="wait" if feasible and adjusted<TODAY_CENTS else "buy_now"
    return {"promotion_probability":float(probability),"ordinary_probability":float(1-probability),
            "today_delivered_cents":TODAY_CENTS,"promotion_future_delivered_cents":PROMOTION_DAY3_CENTS,
            "ordinary_future_delivered_cents":ordinary,"expected_future_delivered_cents":float(expected),
            "declared_delay_cost_cents":delay_cost_cents,"expected_wait_cost_with_delay_cents":float(adjusted),
            "expected_saving_vs_today_cents":float(TODAY_CENTS-adjusted),
            "need_by_day":need_by_day,"waiting_feasible":feasible,"waiting_exclusion_reasons":reasons,
            "synthetic_decision":decision,
            "note":"Risk-neutral expected-cost arithmetic with a declared delay preference and assumed feasibility. A point forecast is not a confirmed promotion; expected savings are not guaranteed savings. The buy-now basket is assumed feasible in this fixture."}

def run():
    return {"case_id":"V1C10-CASE02","currency":"AUD","money_unit":"cents",
            "data_status":"fully synthetic price history, scenario prices, fees and promotion probability",
            "abstract_products":[{"id":"WASH-A","description":"one fixed synthetic washing-powder pack"},
                                 {"id":"CHOC-B","description":"one fixed synthetic Cadbury-chocolate pack; no real SKU or pack-size fact"}],
            "other_goods_cents":OTHER_GOODS_CENTS,"delivery_cents":DELIVERY_CENTS,
            "promotion_prices_cents":[600,300],"ordinary_forecast":ordinary_forecast(),
            "delay_cost_200":compare_timing(delay_cost_cents=200),"delay_cost_400":compare_timing(delay_cost_cents=400),
            "need_before_day3":compare_timing(need_by_day=2),
            "scope":"Regression arithmetic plus a separate assumed uncertain decision model. This non-food-plus-food basket is not the vegan/vegetarian meal or an allergen/nutrition recommendation. No live price service, confirmed sale or product pipeline is implemented."}

def main():
    result=plain(run());path=ROOT/"shopsmart_examples"/"forecast_results.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))

if __name__=="__main__": main()
