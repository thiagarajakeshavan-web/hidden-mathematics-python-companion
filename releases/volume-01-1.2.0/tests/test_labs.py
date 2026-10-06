"""Independent identities and numerical contracts, not visual inspection checks."""
from pathlib import Path
import importlib.util
import math
import sys
import unittest
import numpy as np
from numpy.testing import assert_allclose
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def load(number):
    path = ROOT / f"V1C{number:02d}" / "lab.py"
    spec = importlib.util.spec_from_file_location(f"chapter_{number}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class V1C01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(1)
        cls.result = cls.lab.run()

    def test_cosine_signed_and_orthogonal(self):
        assert_allclose([self.lab.cosine([3,4], x) for x in [[4,3],[-3,-4],[4,-3]]], [.96,-1,0])

    def test_zero_vector_rejected(self):
        with self.assertRaises(ValueError): self.lab.cosine([0,0], [1,2])

    def test_linear_system(self):
        assert_allclose(self.result["linear_system"]["solution"], [3,2])
        self.assertLess(self.result["linear_system"]["residual_norm"], 1e-12)

    def test_pca_covariance_and_variance(self):
        p = self.result["pca"]
        assert_allclose(p["covariance"], np.diag([16/3,4/3]))
        assert_allclose(p["singular_values"], [4,2])
        assert_allclose(p["explained_variance_ratio"], [.8,.2])

    def test_rank_one_error_is_discarded_singular_energy(self):
        p = self.result["pca"]
        self.assertAlmostEqual(p["rank_one_squared_error"], 4.)
        self.assertAlmostEqual(p["rank_one_squared_error"], p["singular_values"][1] ** 2)
        self.assertLess(p["svd_reconstruction_max_error"], 1e-12)

class V1C02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(2)
        cls.result = cls.lab.run()

    def test_scalar_chain_rule(self):
        self.assertEqual(self.lab.derivative(1.), -4.)
        self.assertAlmostEqual(self.result["scalar"]["central_difference"], -4., places=8)

    def test_network_analytic_gradient(self):
        assert_allclose(self.result["network_initial"]["gradient"], [-4,-2,-1.5,-1])

    def test_gradient_independent_numerical_check(self):
        self.assertLess(self.result["maximum_gradient_error"], 1e-8)

    def test_small_simultaneous_update(self):
        update = self.result["simultaneous_updates"][0]
        assert_allclose(update["parameters"], [.54,.52,2.015,.01])
        self.assertAlmostEqual(update["prediction"], 3.234)
        self.assertAlmostEqual(update["loss"], .293378)

    def test_large_step_can_increase_loss(self):
        update = self.result["simultaneous_updates"][1]
        self.assertAlmostEqual(update["loss"], 1.0878125)
        self.assertGreater(update["loss"], self.result["network_initial"]["loss"])

class V1C03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(3)
        cls.result = cls.lab.run()

    def test_bayes_rational_value(self):
        self.assertAlmostEqual(self.lab.posterior(.01), 2/13)
        self.assertAlmostEqual(self.lab.posterior(.1), 2/3)

    def test_constructed_counts_reconcile(self):
        c = self.result["bayes"]["constructed_counts_per_100000"]
        self.assertEqual(sum(c.values()), 100000)
        self.assertAlmostEqual(c["true_positive"] / (c["true_positive"] + c["false_positive"]), self.lab.posterior(.01))

    def test_discrete_moments(self):
        assert_allclose(self.lab.moments([0,1,2],[.2,.5,.3]), [1.1,.49])

    def test_zero_conditioning_event_rejected(self):
        with self.assertRaises(ValueError): self.lab.posterior(0., .9, 0.)

    def test_distribution_examples(self):
        d = self.result["distribution_examples"]
        self.assertAlmostEqual(d["binomial_n5_p04_probability_k3"], math.comb(5,3)*.4**3*.6**2)
        self.assertAlmostEqual(d["poisson_mean3_probability_k2"], math.exp(-3)*9/2)
        self.assertAlmostEqual(d["exponential_rate02_probability_above5"], math.exp(-1))

class V1C04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(4)
        cls.result = cls.lab.run()

    def test_sample_statistics(self):
        a = self.result["inference"]
        self.assertEqual(a["n"], 5)
        self.assertEqual(a["mean"], 50)
        self.assertAlmostEqual(a["sample_sd_ddof1"], math.sqrt(2.5))
        self.assertAlmostEqual(a["standard_error"], math.sqrt(.5))

    def test_t_inference_contract(self):
        a = self.result["inference"]
        assert_allclose(a["mean_confidence_interval"], [48.03675683852244,51.96324316147756], atol=1e-9)
        self.assertAlmostEqual(a["t_statistic"], math.sqrt(8))
        self.assertAlmostEqual(a["two_sided_p_value"], .0474206555843, places=11)

    def test_normal_variance_conventions(self):
        a = self.result["mle"]
        self.assertEqual(a["normal_variance_mle_ddof0"], 2.)
        self.assertEqual(a["unbiased_sample_variance_ddof1"], 2.5)

    def test_bernoulli_mle(self):
        p = 7/10
        derivative = 7/p-3/(1-p)
        self.assertAlmostEqual(derivative, 0.)
        self.assertGreater(self.lab.bernoulli_log_likelihood(p), self.lab.bernoulli_log_likelihood(.5))
        self.assertGreater(self.lab.bernoulli_log_likelihood(p), self.lab.bernoulli_log_likelihood(.9))

    def test_seeded_simulation_shape_and_scale(self):
        sims = self.result["simulations"]
        self.assertEqual(len(sims["clt_repeated_samples"]), 3)
        # These bounds check this fixed fixture, not an LLN/CLT guarantee for every sample.
        for row in sims["clt_repeated_samples"]:
            self.assertEqual(row["replications"], 5000)
            self.assertLess(abs(row["standardized_mean"]), .1)
            self.assertTrue(.8 < row["standardized_variance"] < 1.2)

class V1C05Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(5)
        cls.result = cls.lab.run()

    def test_loss_normalization(self):
        self.assertEqual(self.lab.loss(0), 5.)
        self.assertEqual(self.lab.gradient(0), -5.)

    def test_stable_updates(self):
        assert_allclose([r["w"] for r in self.result["stable"]], [0,1,1.5,1.75,1.875])
        assert_allclose([r["loss"] for r in self.result["stable"]], [5,1.25,.3125,.078125,.01953125])

    def test_boundary_oscillation(self):
        assert_allclose([r["w"] for r in self.result["boundary_oscillation"]], [0,4,0,4,0])

    def test_divergence(self):
        losses = [r["loss"] for r in self.result["divergence"]]
        self.assertTrue(all(a < b for a,b in zip(losses, losses[1:])))

    def test_preconditioning_fixed_example(self):
        c = self.result["conditioning"]
        self.assertEqual(c["condition_number"], 100.)
        self.assertEqual(c["history"][-1]["iteration"], 100)
        self.assertLess(c["history"][-1]["preconditioned_loss"], c["history"][-1]["raw_loss"])

class V1C06Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(6)
        cls.result = cls.lab.run()

    def test_information_values(self):
        a = self.result
        self.assertAlmostEqual(a["entropy_bits"], .8112781244591328)
        self.assertAlmostEqual(a["cross_entropy_bits"], .8832062193464952)
        self.assertAlmostEqual(a["kl_bits"], .0719280948873624)

    def test_kl_identity_and_nonnegativity(self):
        rng = np.random.default_rng(6006)
        for _ in range(20):
            p, q = rng.dirichlet(np.ones(4), size=2)
            kl = self.lab.kl_divergence(p,q)
            self.assertGreaterEqual(kl, -1e-12)
            self.assertAlmostEqual(self.lab.cross_entropy(p,q), self.lab.entropy(p)+kl)

    def test_zero_probabilities(self):
        self.assertEqual(self.lab.entropy([1,0]), 0.)
        self.assertTrue(math.isinf(self.lab.cross_entropy([1,0],[0,1])))

    def test_softmax_stability_and_translation(self):
        p = self.lab.stable_softmax([1000,1001,999])
        self.assertTrue(np.isfinite(p).all())
        self.assertAlmostEqual(p.sum(), 1.)
        assert_allclose(p, self.lab.stable_softmax([0,1,-1]), atol=1e-13)

    def test_log_loss_matches_logsumexp(self):
        p = self.result["softmax"]
        self.assertAlmostEqual(-math.log(p[1]), self.result["true_class_loss_nats"])

class V1C07Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(7)
        cls.result = cls.lab.run()

    def test_exact_unbiased_decomposition(self):
        a = self.result["exact_unbiased"]
        self.assertEqual(a["bias_squared"], 0.)
        self.assertAlmostEqual(a["variance"], 8/3)
        self.assertAlmostEqual(a["expected_squared_error"], 20/3)

    def test_exact_biased_decomposition(self):
        a = self.result["exact_biased"]
        self.assertEqual(a["bias_squared"], 4.)
        self.assertEqual(a["variance"], 0.)
        self.assertEqual(a["expected_squared_error"], 8.)

    def test_hoeffding_sample_size(self):
        n = self.result["hoeffding"]["required_n_M100_epsilon_005"]
        self.assertEqual(n, 1659)
        self.assertLessEqual(200*math.exp(-2*n*.05**2), .05)
        self.assertGreater(200*math.exp(-2*(n-1)*.05**2), .05)

    def test_alpha_selected_only_by_validation_score(self):
        r = self.result["regularization"]
        self.assertEqual(r["selected_alpha"], min(r["validation_scores"], key=lambda x:x["validation_mse"])["alpha"])
        self.assertEqual(r["selected_alpha"], 1.)

    def test_scaler_is_fitted_on_training(self):
        rng = np.random.default_rng(707)
        x,y = self.lab.sample(rng,25)
        fitted = self.lab.model(12,1.).fit(x,y)
        poly = fitted.steps[0][1]
        scaler = fitted.steps[1][1]
        assert_allclose(scaler.mean_, poly.transform(x).mean(axis=0))
        self.assertEqual(scaler.n_samples_seen_, 25)

    def test_finite_ensemble_identity(self):
        for row in self.result["repeated_fits"]["models"].values():
            assert_allclose(row["error_to_noiseless_truth"], row["bias_squared"]+row["variance"], rtol=1e-10, atol=1e-10)

class V1C08Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lab = load(8)
        cls.result = cls.lab.run()

    def test_confusion_and_cost(self):
        a = self.result["threshold_results"][0]
        self.assertEqual([a[k] for k in ["true_positive","false_positive","false_negative","true_negative"]],[2,1,1,4])
        self.assertAlmostEqual(a["f1"], 2/3)
        self.assertEqual(a["total_cost"], 12.)

    def test_threshold_ties_included(self):
        a = self.result["threshold_results"][1]
        self.assertEqual(a["true_positive"],3)
        self.assertEqual(a["total_cost"],4.)

    def test_auc_rank_and_ties(self):
        self.assertAlmostEqual(self.result["roc_auc"],12/15)
        self.assertAlmostEqual(self.result["pairwise_auc_crosscheck"],12/15)
        self.assertEqual(self.lab.pairwise_auc(np.array([0,1]),np.array([.5,.5])),.5)

    def test_average_precision_is_recall_weighted_precision(self):
        self.assertAlmostEqual(self.result["average_precision"],(1+2/3+3/5)/3)

    def test_brier_and_log_loss_direct(self):
        y,p = self.lab.Y,self.lab.P
        self.assertAlmostEqual(self.result["brier_score"],np.mean((p-y)**2))
        self.assertAlmostEqual(self.result["log_loss_nats"],-np.mean(y*np.log(p)+(1-y)*np.log1p(-p)))

    def test_calibration_bins_partition_data(self):
        bins = self.result["calibration_bins"]
        self.assertEqual(sum(b["count"] for b in bins),8)
        row = next(b for b in bins if b["lower_inclusive"]==.6)
        self.assertEqual(row["count"],1)
        self.assertEqual(row["observed_fraction_positive"],1.)

    def test_regression(self):
        r = self.result["regression"]
        self.assertAlmostEqual(r["mae"],7/3)
        self.assertAlmostEqual(r["mse"],17/3)
        self.assertAlmostEqual(r["r_squared"],1-17/200)

    def test_group_leakage_evidence(self):
        splits = self.result["group_leakage"]["splits"]
        self.assertGreater(splits["random_row_split"]["overlapping_groups"],0)
        self.assertEqual(splits["unseen_group_split"]["overlapping_groups"],0)
        self.assertGreater(splits["random_row_split"]["test_accuracy"],splits["unseen_group_split"]["test_accuracy"])

    def test_chronology_does_not_cure_future_features(self):
        a = self.result["temporal_leakage"]
        self.assertLess(a["train_end_time"],a["test_start_time"])
        self.assertEqual(a["rows_with_future_feature_unavailable_at_decision"],500)
        self.assertEqual(a["chronological_leaked_accuracy"],1.)
        self.assertLess(a["chronological_safe_accuracy"],.7)


class ExtensionTests(unittest.TestCase):
    def test_batch_matches_scalar_cosines(self):
        lab=load(1);r=lab.run()
        assert_allclose(r["batch_cosines"],[row["cosine"] for row in r["similarities"]])

    def test_invalid_probability_mass_rejected(self):
        lab=load(3)
        for p in [[-.1,.5,.6],[.2,.2,.2]]:
            with self.assertRaises(ValueError): lab.moments([0,1,2],p)

    def test_invalid_t_sample_rejected(self):
        lab=load(4)
        with self.assertRaises(ValueError): lab.mean_inference([1.])
        with self.assertRaises(ValueError): lab.mean_inference([1.,1.])

    def test_finite_difference_and_minibatch_gradient(self):
        lab=load(5);r=lab.run()
        for row in r["gradient_checks"]:
            self.assertAlmostEqual(row["central_difference_at_zero"],-5.,places=6)
        self.assertAlmostEqual(np.mean(r["individual_gradients_at_zero"]),r["full_gradient_at_zero"])

    def test_mutual_information_and_xor(self):
        r=load(6).information_extension()
        self.assertAlmostEqual(r["mutual_information_bits"],.2780719051126377)
        self.assertEqual(r["xor"]["I_X1_Y_bits"],0.)
        self.assertEqual(r["xor"]["I_X2_Y_bits"],0.)
        self.assertEqual(r["xor"]["I_pair_Y_bits"],1.)

    def test_softmax_gradient_and_perplexity(self):
        r=load(6).run()
        self.assertAlmostEqual(np.sum(r["logit_gradient"]),0.,places=12)
        self.assertAlmostEqual(r["single_token_perplexity"],1/r["softmax"][1])

    def test_information_invalid_inputs(self):
        lab=load(6)
        with self.assertRaises(ValueError): lab.entropy([.5,.5],base=1.)
        with self.assertRaises(ValueError): lab.entropy([.5,.4])

    def test_scalar_penalties(self):
        lab=load(7)
        self.assertEqual(lab.scalar_penalties(3)["l1_solution"],2.)
        self.assertEqual(lab.scalar_penalties(3)["l2_solution"],1.5)
        self.assertEqual(lab.scalar_penalties(.6)["l1_solution"],0.)
        self.assertEqual(lab.scalar_penalties(.6)["l2_solution"],.3)

    def test_absent_class_auc_is_explicit(self):
        lab=load(8)
        with self.assertRaises(ValueError): lab.pairwise_auc(np.array([0,0]),np.array([.1,.2]))

    def test_undefined_precision_and_recall_are_null(self):
        lab=load(8)
        r=lab.threshold_metrics(np.array([0,1]),np.array([.1,.1]),.5)
        self.assertIsNone(r["precision"])
        self.assertEqual(r["recall"],0.)
        r=lab.threshold_metrics(np.array([0,0]),np.array([.1,.1]),.5)
        self.assertIsNone(r["recall"])
        self.assertIsNone(r["f1"])

if __name__ == "__main__":
    unittest.main()
