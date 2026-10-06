# Additive ShopSmart worked examples

Author: Keshavan Thiagaraja · Release 1.1.0-author-review

These two requested worked examples extend Chapters 5 and 10 without changing the original Chapter 1–8 source, test or result files. They are separate mathematical fixtures, not a working retail platform. All money is in Australian dollars (AUD); source calculations use cents to preserve exact basket arithmetic.

## Run

Using the virtual environment's Python from the root quickstart:

```sh
python shopsmart_examples/basket_comparison.py
python shopsmart_examples/forecast_timing.py
python -m unittest discover -s tests -p test_shopsmart_cases.py -v
```

The full `run_all.py` also runs both cases. Outputs are `basket_results.json` and `forecast_results.json` in this folder.

## V1C05-CASE02: compare single-store and merged baskets

Assume three approved equivalent abstract product lines, P1/P2/P3, exactly one purchased pack each. These are not actual product quotations, a complete dinner for five or a nutrition/allergen recommendation.

| Assumed retailer | P1 | P2 | P3 | Goods total | Single-store fees | Delivered total |
|---|---:|---:|---:|---:|---:|---:|
| Coles | A$8 | A$11 | A$10 | A$29 | A$4 | A$33 |
| Woolworths | A$10 | A$7 | A$12 | A$29 | A$7 | A$36 |
| ALDI | A$9 | A$10 | A$6 | A$25 | A$9 | A$34 |

For every mixed-store plan, assume pickup costs A$2 per visited store plus one hypothetical A$8 consolidated-courier charge. These are teaching assumptions, not the retailers' or a courier's actual fees or verified service terms.

Choosing the cheapest product separately gives P1 from Coles, P2 from Woolworths and P3 from ALDI: goods A$21, fees A$14, total A$35. Exhaustive enumeration covers all 27 assignments. Coles-only at A$33 is the global minimum under these assumptions. There are 13 assignments strictly below A$40; none is strictly below A$33. A strict “under” budget excludes equality.

The function excludes unavailable stock, ineligible products and unavailable store/consolidation services. A flagged substitution is excluded unless specifically approved, and it still must satisfy the supplied eligibility flag. Unknown conditions must be marked false for review, not assumed safe or available. Defaults are explicitly favorable synthetic fixture assumptions; the program does not verify live facts.

## V1C10-CASE02: a forecast is separate from a timing decision

This is a different generic price basket. It includes one fixed synthetic washing-powder pack WASH-A and one fixed synthetic Cadbury-chocolate pack CHOC-B. No real SKU, pack size or price fact is asserted. The basket is not a vegan/vegetarian meal and implies no allergy suitability.

At relative days `−6,−3,0`, assumed WASH-A prices are A$8, A$9, A$10; CHOC-B is always A$6. OLS fits WASH-A as `p(t)=10+t/3`, giving A$11 at day 3; CHOC-B's ordinary-state forecast remains A$6. Only observations available at the forecast origin `t=0` enter the fit. Three observations cannot validate a real forecasting model.

Other basket goods remain A$11 and delivery remains A$6:

- Buy today: `10+6+11+6 = A$33`
- Assumed day-3 promotion: `6+3+11+6 = A$26`
- Ordinary day-3 forecast: `11+6+11+6 = A$34`

The promotion prices and probability `0.6` are separately supplied scenario assumptions. They are not learned from those three observations, verified retailer promotions or calibrated model probabilities. The ordinary-state probability is `0.4`.

Expected future delivered cost is `0.6×26 + 0.4×34 = A$29.20`. With the shopper's declared A$2 delay cost, the risk-neutral expected comparison is A$31.20 versus A$33 now, an expected A$1.80 benefit to waiting. With A$4 delay cost, the wait total becomes A$33.20, so the fixture chooses buy-now. A tie defaults to buy-now. These are arithmetic outputs, not promises of savings.

Waiting is infeasible if the need-by deadline is before day 3, or if future stock, eligibility or service availability is not established by the supplied flags. A lower expected price never overrides these constraints. The buy-now basket is assumed feasible in this small fixture. Real decisions also require verified products, timestamps, stock, fees, service terms, restrictions, uncertainty and user approval for purchases.

## Typed, voice and uploaded lists: proposed input contract

A complete platform could accept a typed list, voice request or uploaded shopping list, then confirm a shared structured basket: exact product/variant, whole-pack quantity, acceptable equivalents, restrictions, currency, delivery location and deadline. Ambiguous recognition, duplicate lines, pack-size differences and proposed substitutions would need review before optimization.

This companion receives fixed structured teaching inputs only. It does not implement speech recognition, OCR, document parsing, live retailer-price feeds, stock verification, nutrition/allergen assessment, payment, order placement, multi-store pickup or courier integration. No named provider's partnership or service capability is asserted.
