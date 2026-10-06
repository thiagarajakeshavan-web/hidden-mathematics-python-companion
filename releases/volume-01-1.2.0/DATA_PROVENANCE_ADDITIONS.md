# Data provenance: 1.2.0 additions

Author: Keshavan Thiagaraja. Recorded 2026-10-05 UTC.

## Wholly synthetic commercial fixtures

`shopsmart_scenarios/data/grocery30.csv` contains 30 author-created requested lines and 90 fictitious matched offers, including exact quantities, pack sizes, integer-cent prices, stock counts and cold-chain flags. Store names provide familiar teaching context; no price, product match, stock or service offer came from a retailer.

`timing_scenarios.json` contains two fictional announced promotions, explicit relative validity days, assumed joint scenario probabilities and pack-price/stock changes. “Confirmed within fiction” is never a real retailer announcement. No model is trained and no scenario weight is statistically estimated. Actual prices, expiry, stock and fulfillment remain unknown.

`dinner5.json` contains a fictional 13-line, 14-pack cooking kit and invented product-eligibility evidence. No real person's health information or actual product/allergen clearance is stored. The full ingredient quantities, leftover arithmetic, included fees and pantry boundaries are explicit. UNKNOWN evidence fails closed in the model.

## Four factual nutrient reference values

The only non-synthetic values added are protein 7.3 g, dietary fibre 4.1 g, iron 1.63 mg and folate 14 µg per 100 g for FSANZ AFCD F005177, lentil boiled in unsalted water and drained. The primary record was checked on 2026-10-05: https://www.foodstandards.gov.au/science-data/food-nutrient-databases/afcd/search/food/F005177 . These are recipe-derived reference values. No full third-party dataset or webpage is redistributed.

The assumed cooked-and-drained batch weight of 1000 g is a separate fictional input, not a verified yield from the purchased 500 g dry pack. The calculation scales only the reference lentil component; whole-meal nutrition, nutrient adequacy and clinical recommendations are not established. A changed food record, nutrient unit or reference value requires separate verification; the program rejects such silent substitutions under the existing attribution.

FSANZ allergen-label guidance and ASCIA avoidance guidance inform scope statements; they do not clear any fictional or real product. Links and access date are in both reader guides.

## Mathematical fixtures

V1C04-CASE02 uses seven successes in ten constructed Bernoulli trials and illustrative Beta priors. V1C07-CASE02 exactly enumerates two binary targets after one fixed observation. Both use exact rational arithmetic and do not measure real learner performance.

## Rights and limits

No secrets, personal/customer data, manuscripts, investor sources, credentials, account access or source-confidential content are included. No new licence was selected for the author's work. The new executable modules require only Python's standard library; the pre-existing lab dependencies remain as documented in DEPENDENCIES.md. Source citations and factual reference values do not imply endorsement or a retailer/courier/health partnership.
