# New ShopSmart teaching cases: English reader guide

Author: **Keshavan Thiagaraja**. Companion release: **1.2.0-author-review**.

These offline cases extend the existing Volume 1 labs without replacing their examples. All shopping prices, promotions, stock, matched products, fees, routes and ingredient-label assessments are invented. Coles, Woolworths and ALDI are familiar names in a fictional comparison; none supplied these offers or promised these services. No retail API, courier integration, real-time forecast, allergy-safe product recommendation, order or purchase is implemented. Public GitHub publication remains pending.

## Case map

- **V1C05-CASE03:** 30 requested grocery lines, whole packs and total delivered cost
- **V1C10-CASE03:** the same list today, after two days and after three days
- **V1C05-CASE04:** one vegan home-cooked dinner for five people, strictly below A$40 in the fixture
- **V1C04-CASE02:** the small MLE, MAP and posterior-mean bridge, in `../V1C04/CASE02/`
- **V1C07-CASE02:** a finite No Free Lunch symmetry illustration, in `../V1C07/CASE02/`

The earlier V1C05-CASE02 and V1C10-CASE02 remain unchanged. Chapter 14 remains a brief preview without a required lab. One implementation serves the separate English and Tamil books.

## 1. Compare the complete 30-line list

Open `data/grocery30.csv`. Each row records a requested quantity, a unit, and one matched offer from each store: pack size, whole-pack price and available pack count. These are 30 different requested lines, not necessarily 30 purchased packs. Pasta and chocolate demonstrate why a lower unit price or smaller sticker price may not yield the lowest payable line cost.

Each full line goes to exactly one store. If the requested amount is r and that store's pack size is p, buy ceil(r/p) packs. The unused amount remains visible. The example assumes the shopper has approved each matched equivalent; it does not silently approve substitutions or interpret an uploaded or spoken list.

The optimizer retains the cheapest prefix for each exact set of stores used. It then adds that set's complete fixed fees. There are seven nonempty store subsets. At most 30 × 3 × 8 state transitions are needed, rather than evaluating 3^30 assignments. The proof depends on independent line costs, distinct stock per item and fees depending only on the final used-store set. This is an exact optimizer for that stated model, not for every real shopping rule.

All seven delivered totals, in AUD:

| Exact stores used | Payable total |
|---|---:|
| Coles | 116.30 |
| Woolworths | 113.70 |
| ALDI | 109.20 |
| Coles + Woolworths | 113.90 |
| Coles + ALDI | 112.10 |
| Woolworths + ALDI | 110.30 |
| All three | 111.00 |

The fixed example that assigns the first ten lines to Coles, the next ten to Woolworths and the final ten to ALDI costs A$115.70. The cheapest three-store allocation is 8/11/11 and costs A$111.00. ALDI-only wins overall at A$109.20: lower shelf prices do not automatically offset extra stops and handling. The allocation 10/10/10 is an example, never a compulsory optimum.

Single-store fees are A$6.00, A$6.50 and A$5.00 respectively. A merged route assumes A$8.00 base delivery, A$1.00 handling per used store and A$2.00 per additional stop: A$12.00 for two stores or A$15.00 for three. These totals assume all mandatory fees and taxes already included, no membership requirement and no minimum order. Nonzero minimum-spend and membership rules are rejected because the state representation does not support them. A real implementation must model them rather than ignore them.

Service area, pickup availability, overlapping windows, route timing and cold-chain capability are explicit assumed gates. Unknown or failed gates exclude the route. There is no real route computation. Missing or unknown stock, unknown prices and unapproved equivalence exclude affected offers; an incomplete basket is not ranked as a cheaper complete one.

Experiment: change only merged base delivery from A$8.00 to A$5.00. The best plan becomes the two-store Woolworths + ALDI option at A$107.30, saving A$1.90 against the original best single-store basket. This sensitivity result is tested. It illustrates why the answer depends on complete fees.

## 2. Decide whether waiting is worth it

`data/timing_scenarios.json` gives two explicitly fictional announced promotions valid on days two and three, plus assumed joint downside, central and upside outcomes. “Confirmed” means confirmed inside this invented scenario only; no retailer announcement was retrieved. Other future prices are uncertain scenario inputs, not trained or calibrated predictions.

| Purchase day | Expected payable | Waiting penalty | Expected decision cost | Net expected saving vs today |
|---|---:|---:|---:|---:|
| Today | 109.20 | 0.00 | 109.20 | 0.00 |
| Day 2 | 106.10 | 3.00 | 109.10 | 0.10 |
| Day 3 | 101.38 | 4.50 | 105.88 | 3.32 |

The penalty is A$1.50 per waiting day and represents an assumed inconvenience preference; it is not a checkout charge. Day-two outcome weights are 20%/60%/20%; day-three weights are 20%/50%/30%. Expected payable is the weighted sum of complete optimized baskets in those joint states. Choose a day now, then select stores after that day's prices and stock are observed. This adaptive allocation assumption must not be confused with knowing the future today.

The scenario payable ranges are A$99.30–112.90 on day two and A$92.50–119.90 on day three. They are scenario envelopes, not statistical prediction intervals. Risk-neutral expected cost selects day three; a minimax rule selects today. Thus the expected A$3.32 benefit is not a guaranteed saving. The need-by deadline can forbid waiting, and a higher inconvenience penalty can favour today. If any positively weighted state has no complete basket, its expected comparison is blocked rather than averaging away unmet demand. Stock, expiry and quality in real life need fresh evidence; this tiny scenario set does not cover every risk.

## 3. Buy a whole kit for one vegan dinner for five

The fixture in `data/dinner5.json` prepares lentil, tomato and spinach stew with rice, broccoli and carrots. All thirteen ingredient lines are priced, including oil and spices. Only drinking water is assumed available. Equipment, household energy and water charges are outside the grocery-checkout budget.

| Ingredient | Used for five | Whole purchase | Cost, AUD |
|---|---|---|---:|
| Dry rice | 350 g | 1 × 1000 g | 2.50 |
| Dry lentils | 500 g | 1 × 500 g | 2.40 |
| Chopped tomatoes | 800 g | 2 × 400 g | 2.00 |
| Onions | 300 g | 1 × 1000 g | 2.50 |
| Carrots | 400 g | 1 × 1000 g | 2.00 |
| Spinach | 250 g | 1 × 250 g | 2.00 |
| Broccoli | 500 g | 1 × 500 g | 2.50 |
| Garlic | 20 g | 1 × 100 g | 1.00 |
| Lemon | 1 | 1 pack of 3 | 1.50 |
| Cooking oil | 30 ml | 1 × 500 ml | 3.00 |
| Cumin | 6 g | 1 × 35 g | 1.80 |
| Paprika | 6 g | 1 × 35 g | 1.80 |
| Black pepper | 2 g | 1 × 40 g | 1.80 |

Goods cost A$26.80; assumed delivery and handling add A$6.00. The payable A$32.80 is strictly below A$40, with A$7.20 headroom. Fourteen whole packs are purchased. The used-ingredient accounting allocation is 18077/14 cents, about A$12.91 before fees; that amount cannot buy the kit from an empty pantry. Leftovers remain explicitly recorded. At exactly the budget ceiling the strict-under-budget gate fails.

Cook the lentils in unsalted water according to pack directions and drain. Cook the rice separately. Soften onions and carrots with 20 ml oil; add garlic, cumin, paprika and pepper. Add both cans of tomatoes and water as needed; simmer until the carrots are tender. Add cooked lentils and spinach and heat through. Steam the broccoli; dress with the remaining 10 ml oil and lemon. Divide everything into five portions. Full quantities and steps are also saved in the fixture and output. This is one home-cooked dinner, not five days or a restaurant order; portion needs vary.

### Dietary eligibility is a hard gate

The vegan requirement is separate from vegetarian eligibility. Peanut is also separate from the named tree nuts. The broader fixture profile excludes peanut plus almond, Brazil nut, cashew, hazelnut, macadamia, pecan, pistachio, pine nut and walnut. “Nut-free” by itself is too ambiguous for the input contract.

Every required allergen needs current ingredient evidence and resolved cross-contact evidence. UNKNOWN, missing, stale, conflicting or “may contain” input blocks the relevant candidate. The absence of an ingredient declaration alone cannot establish safety. A cheaper price never bypasses a gate. The kitchen review is another explicit fixture gate. Even when every synthetic check passes, actual-product clearance remains false: no real product, substitution or kitchen has been reviewed. Actual use needs current label and cross-contact information and appropriate human review. No real person's allergy is recorded or transmitted.

### A scoped nutrient calculation

FSANZ's AFCD food F005177 is lentil boiled in unsalted water and drained. Its reference values per 100 g are protein 7.3 g, dietary fibre 4.1 g, iron 1.63 mg and folate 14 µg. These are recipe-derived database values, not an assay of our meal.

For an illustrative measured cooked-and-drained mass of 1000 g, multiply by ten, then divide by five portions. The lentil component contributes an estimated 14.6 g protein, 8.2 g fibre, 3.26 mg iron and 28 µg folate per portion under these assumptions. The 1000 g is a separate assumed cooked-weight input; no validated conversion from the purchased 500 g dry lentils is claimed. Weigh the actual batch and use a matching reference form before estimating it. Whole-meal totals, nutrient adequacy and clinical targets remain unknown; the program does not invent them or promise a health outcome.

## 4. MLE, MAP and posterior mean

`V1C04-CASE02` uses seven successes in ten constructed Bernoulli trials. MLE = 7/10. With an illustrative Beta(2,2) prior, the posterior is Beta(9,5), the interior MAP is 8/12 = 2/3 and the posterior mean is 9/14. With a uniform Beta(1,1) prior, MAP equals MLE for these observations. The Beta(a,b) interior-mode formula requires a > 1 and b > 1; boundary cases are rejected by this small hook. A prior does not automatically improve predictions.

## 5. A bounded No Free Lunch illustration

`V1C07-CASE02` fixes X = {a,b} and observes f(a)=0. Uniformly weighted binary target functions leave two equally likely unseen labels. Always predicting zero or always predicting one at b each has average 0–1 error 1/2. Randomization with probability q of predicting one also gives (1/2)q + (1/2)(1−q) = 1/2. These narrow symmetry assumptions matter: real task distributions need not be uniform over all targets, and useful inductive biases can make learners perform differently. This is a small illustration, not a general proof or a claim that practical learning is pointless.

## Run and inspect

From the companion root, after following the existing dependency setup:

```sh
python run_additions.py
python -W error -m unittest discover -s tests -v
python verify_manifest.py
```

The new cases use only Python's standard library. The full pre-existing suite still needs the pinned dependencies in `requirements.txt`. `run_all.py` remains the original 13-lab/two-case runner; `run_additions.py` refreshes only these five additions. Inspect the saved JSON outputs, change one documented assumption in a copy, and rerun tests. Tests include exhaustive small-instance comparison against the DP, whole-pack rounding, all seven subsets, uncertainty arithmetic, unknown-eligibility rejection, exact budget boundaries and nutrient unit scaling.

## Primary references checked 5 October 2026

- [FSANZ AFCD F005177, cooked drained lentil](https://www.foodstandards.gov.au/science-data/food-nutrient-databases/afcd/search/food/F005177)
- [FSANZ allergen labelling for consumers](https://www.foodstandards.gov.au/consumer/labelling/allergen-labelling), including separately named tree nuts and voluntary precautionary statements
- [ASCIA dietary avoidance for food allergy](https://www.allergy.org.au/patients/food-allergy/ascia-dietary-avoidance-for-food-allergy)

No new licence for the author's code has been selected. Few factual nutrient values and source links are included; third-party pages are not bundled. This is a teaching implementation and author-review release, not publication, live shopping, purchasing or health advice.
