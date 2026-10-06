# V2C15-CASE02: Adaptive optimiser arithmetic

This case feeds the SAME supplied gradients 2 then −1 to AdaGrad, uncentred RMSProp and Adam. It does not train three networks or establish a performance winner. Every method starts at parameter 0 with zero accumulators, learning rate 0.1 and epsilon 1e-8. RMSProp uses beta2=0.9; Adam uses beta1=beta2=0.9 for transparent arithmetic, not as recommended defaults.

All denominators add epsilon AFTER the square root. AdaGrad accumulates all squared gradients; RMSProp uses an exponentially weighted average with no centring, momentum or bias correction; Adam combines signed and squared moving averages and divides by 1−beta1^t and 1−beta2^t. There is no weight decay, gradient clipping, schedule, AMSGrad or AdamW.

The second parameter values are −0.05527864015000421 (AdaGrad), −0.16878580703585389 (RMSProp), and −0.1270604029857565 (Adam). Adam still moves negatively after the gradient becomes negative because its signed first moment remains positive. Inspect the intermediate denominators and signed changes rather than interpreting a smaller parameter as a better result.

Change epsilon to 0.25 and verify its placement by hand; replace the second gradient by zero and inspect remembered momentum. The new unit tests derive expected updates from independent scalar formulas. Separate reviewer tests also use 60-digit Decimal arithmetic and a mixed-gradient sweep. Zero/nonfinite controls, invalid decay factors and zero gradients are checked.

The implementation is src/volume2_companion/chapter15_optimizers.py. It accepts a finite scalar-gradient sequence and starts a fresh trace per call. It is not a vector optimiser object, checkpoint system or automatic-differentiation training loop. Real optimisation recomputes gradients at each method’s current parameters, so different methods need not see the same later gradients.

From the companion root:

    python run_cases.py --chapter 15 --case 2 --verify

Or run this case’s run.py from any folder. Preserve fixture.json before changes. expected.json records executed output; changing it is not independent verification. No network, downloads, API keys or credentials are used.
