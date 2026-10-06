# V1C09 · Types of Machine Learning

Primary case: `V1C09-CASE01` · Companion release: `1.1.0-author-review`

## Purpose and inputs

Four deliberately small demonstrations distinguish the source of supervision and the mathematical objective. These are constructed arithmetic fixtures, not trained ShopSmart services. The proposed B2C/B2B platform provides context only.

- Supervised targets `[2,4,6]`, predictions `[3,4,5]`
- Unsupervised one-dimensional observations `[1,2,8,9]`, initial centers `[1,8]`
- Self-supervised masked observed token `rice`, supplied predicted probability `0.7`
- Simulated rewards `[5,4]` versus `[7,1]`, discount `0.9`; one Q-learning update

The small CSV files mirror the relevant literals in `lab.py`. No text corpus is downloaded and no neural network is trained.

## Run and test

From the companion root, using the environment's Python described in the quickstart:

```sh
python V1C09/lab.py
python -m unittest discover -s tests -p test_classical_labs.py -k V1C09 -v
```

## Expected results

MSE `2/3`; updated k-means centers `1.5,8.5`; inertia decreases from `2` to `1`. Masked-token negative log likelihood is `−ln(0.7)=0.35667494393873245` nats. The supplied reward-sequence returns are `8.6` and `7.9`. Updating `Q=2` with learning rate `0.5`, reward `1`, discount `0.9` and next maximum Q `4` gives `3.3`.

`results.json` records the executed output. Tests independently check the objectives, endpoints and invalid inputs. A reward-sequence comparison is not evidence that a learned policy is good. This lab does not implement or evaluate semi-supervised learning; that paradigm is discussed conceptually in the chapter.

## Experiment and limits

Change the discount to `0` and `1`, then explain the changed ranking. Refit k-means after adding a point and distinguish the objective from a business segment name. A masked-token loss is self-supervised because the target is derived from the observed data; a supplied probability does not establish a language model's training quality. Inventory simulations never authorize live purchases or experiments involving allergen restrictions.
