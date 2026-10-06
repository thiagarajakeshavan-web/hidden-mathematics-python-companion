"""Numerical, split-isolation, calibration and regression tests for Chapters 9--13."""
from pathlib import Path
import importlib.util
import json
import sys
import unittest
import numpy as np
from numpy.testing import assert_allclose
from sklearn.metrics import log_loss

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import plain
from classical_common import classification_data, binary_metrics, three_way_indices

def load(number):
    spec=importlib.util.spec_from_file_location(f"classical_{number}",ROOT/f"V1C{number:02d}"/"lab.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def check_partition(testcase, partitions, n):
    arrays=[np.asarray(indices) for indices in partitions.values()]
    testcase.assertEqual(sum(len(a) for a in arrays), n)
    assert_allclose(np.sort(np.concatenate(arrays)), np.arange(n))
    for i,left in enumerate(arrays):
        testcase.assertEqual(len(left),len(np.unique(left)))
        for right in arrays[i+1:]: testcase.assertEqual(len(np.intersect1d(left,right)),0)

class V1C09Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lab=load(9);cls.result=cls.lab.run()

    def test_supervised_mse(self):
        self.assertAlmostEqual(self.result["supervised"]["mse"],2/3)
        assert_allclose(self.result["supervised"]["squared_errors"],[1,0,1])

    def test_kmeans_centers_labels_and_objective(self):
        r=self.result["clustering"]
        assert_allclose(r["centers_after_update"],[1.5,8.5]);assert_allclose(r["labels"],[0,0,1,1])
        self.assertEqual(r["initial_inertia"],2.);self.assertEqual(r["inertia_final"],1.)

    def test_self_supervised_nll(self):
        r=self.result["self_supervised"]
        self.assertAlmostEqual(r["negative_log_likelihood_nats"],-np.log(r["predicted_probability"]))

    def test_discounted_returns(self):
        self.assertAlmostEqual(self.lab.discounted_return([5,4],.9),8.6)
        self.assertAlmostEqual(self.lab.discounted_return([7,1],.9),7.9)
        self.assertEqual(self.lab.discounted_return([5,4],0),5)
        self.assertEqual(self.lab.discounted_return([5,4],1),9)

    def test_q_update(self):
        self.assertAlmostEqual(self.result["reinforcement"]["q_updated"],3.3)
        self.assertEqual(self.lab.q_learning_update(2,0,1,.9,4),2)
        self.assertAlmostEqual(self.lab.q_learning_update(2,1,1,.9,4),4.6)

    def test_invalid_rewards_and_parameters_rejected(self):
        for rewards,gamma in [([], .9),([np.nan],.9),([1],1.1),([[1]],.9)]:
            with self.assertRaises(ValueError): self.lab.discounted_return(rewards,gamma)
        for rate,gamma in [(-.1,.9),(.5,-.1),(1.1,.9)]:
            with self.assertRaises(ValueError): self.lab.q_learning_update(2,rate,1,gamma,4)

class V1C10Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lab=load(10);cls.result=cls.lab.run()

    def test_ols_independent_lstsq(self):
        x=self.lab.X_TRAIN;y=self.lab.Y_TRAIN
        b,w=np.linalg.lstsq(np.column_stack([np.ones(len(x)),x]),y,rcond=None)[0]
        r=self.result["regression_fixture"]
        assert_allclose([r["intercept"],r["slope"]],[b,w]);assert_allclose([b,w],[1.5,.8])
        self.assertAlmostEqual(r["training_sse"],1.8)

    def test_exact_heldout_regression_metrics(self):
        r=self.result["regression_fixture"]
        assert_allclose(r["test_prediction"],[5.5,6.3])
        for key,value in {"mae":.6,"mse":.37,"rmse":np.sqrt(.37),"r_squared":.63}.items():
            self.assertAlmostEqual(r["test_metrics"][key],value)
        self.assertAlmostEqual(r["baseline_test_metrics"]["mse"],7.25)

    def test_gradient_by_finite_difference(self):
        x=self.lab.X_TRAIN;y=self.lab.Y_TRAIN
        def loss(b,w): return np.mean((b+w*x-y)**2)/2
        h=1e-6;numeric=[(loss(h,0)-loss(-h,0))/(2*h),(loss(0,h)-loss(0,-h))/(2*h)]
        r=self.result["regression_fixture"]["gradient"]
        assert_allclose([r["db"],r["dw"]],numeric,atol=1e-8)
        assert_allclose([r["updated_intercept"],r["updated_slope"]],[.35,.975])
        self.assertAlmostEqual(r["updated_loss"],.49796875)

    def test_ridge_penalty_convention(self):
        r=self.result["regression_fixture"]["ridge"]
        self.assertAlmostEqual(r["slope"],4/(5+5));self.assertAlmostEqual(r["intercept"],2.5)

    def test_logistic_supplied_parameters(self):
        r=self.result["logistic_fixture"]
        assert_allclose(r["probabilities"],[.23147521650098238,.5,.7685247834990175])
        self.assertAlmostEqual(r["log_loss_nats"],.40657070507866927)
        self.assertAlmostEqual(r["odds_ratio_per_unit"],np.exp(.8))
        self.assertAlmostEqual(r["at_x4_y1_dw"],4*r["at_x4_y1_db"])

    def test_regression_train_test_partition(self):
        check_partition(self,self.result["heldout_regression"]["split_indices"],400)

    def test_regression_scaler_and_baseline_use_train_only(self):
        r=self.result["heldout_regression"];x,y=self.lab.regression_data();train=r["split_indices"]["train"]
        assert_allclose(r["training_scaler_mean"],x[train].mean(axis=0))
        self.assertEqual(r["scaler_n_samples_seen"],300)
        self.assertAlmostEqual(r["baseline_training_mean"],y[train].mean())
        self.assertFalse(np.allclose(r["training_scaler_mean"],x.mean(axis=0)))

    def test_classification_train_test_partition_and_scaler(self):
        r=self.result["heldout_classification"];x,y=classification_data(1011,800);train=r["split_indices"]["train"]
        check_partition(self,r["split_indices"],800)
        assert_allclose(r["training_scaler_mean"],x[train].mean(axis=0))
        self.assertEqual(r["scaler_n_samples_seen"],600)
        self.assertAlmostEqual(r["baseline_training_prevalence"],y[train].mean())

    def test_fixed_synthetic_metric_regression(self):
        r=self.result["heldout_regression"]
        self.assertAlmostEqual(r["test_linear_regression"]["rmse"],1.9363842742423614,places=8)
        self.assertLess(r["test_linear_regression"]["rmse"],r["test_training_mean_baseline"]["rmse"])
        c=self.result["heldout_classification"]
        self.assertAlmostEqual(c["test_logistic_regression"]["log_loss_nats"],.4698544444466495,places=8)

class V1C11Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lab=load(11);cls.result=cls.lab.run()

    def test_unsmoothed_bayes_counts(self):
        r=self.result["naive_bayes_fixture"]
        assert_allclose(r["unsmoothed_scores_late_on_time"],[.12,.015])
        self.assertAlmostEqual(r["late_probability_unsmoothed"],8/9)
        self.assertAlmostEqual(r["sklearn_late_probability_unsmoothed"],8/9)

    def test_laplace_features_not_class_priors(self):
        r=self.result["naive_bayes_fixture"]
        self.assertAlmostEqual(r["late_probability_smoothed"],16/19)
        self.assertAlmostEqual(r["sklearn_late_probability_smoothed"],16/19)
        assert_allclose(r["smoothed_class_priors_on_time_late"],[.75,.25])

    def test_knn_geometry(self):
        r=self.result["knn_fixture"]
        assert_allclose(r["raw_distances"],[100,2,np.sqrt(6401)])
        assert_allclose(r["scaled_distances"],[1,2,np.sqrt(1.64)])
        self.assertEqual(r["nearest_raw_label"],0);self.assertEqual(r["nearest_scaled_label"],1)
        self.assertAlmostEqual(r["k3_positive_fraction"],2/3)

    def test_svm_margin_support_and_hinge(self):
        r=self.result["svm_fixture"]
        assert_allclose([r["w"],r["b"],r["margin_width"]],[1,0,2])
        assert_allclose(r["support_vectors"],[-1,1]);assert_allclose(r["functional_margins"],[2,1,1,2])
        self.assertAlmostEqual(r["hinge_loss"],1.2)

    def test_rbf_and_cost_threshold(self):
        r=self.result["svm_fixture"]
        self.assertAlmostEqual(r["rbf_value"],np.exp(-1));self.assertEqual(r["ideal_cost_threshold"],.2)

    def test_three_way_partition(self):
        r=self.result["heldout_comparison"]
        check_partition(self,r["split_indices"],1000)
        self.assertEqual(r["split_sizes"],{"train":500,"calibration":250,"test":250})

    def test_scaling_never_sees_calibration_or_test(self):
        r=self.result["heldout_comparison"];x,y=classification_data(1111,1000);train=r["split_indices"]["train"]
        for scaler in r["base_scalers"].values():
            assert_allclose(scaler["mean"],x[train].mean(axis=0));self.assertEqual(scaler["n_samples_seen"],500)

    def test_frozen_calibration_retains_base_and_real_fitted_parameters(self):
        x,y=classification_data(1111,1000);parts=self.result["heldout_comparison"]["split_indices"]
        base,calibrated=self.lab.fit_classifiers(x,y,parts["train"],parts["calibration"])
        for name in base:
            pair=calibrated[name].calibrated_classifiers_[0]
            self.assertIs(pair.estimator.estimator,base[name])
            self.assertTrue(np.isfinite([pair.calibrators[0].a_,pair.calibrators[0].b_]).all())
        self.assertEqual(base["rbf_svm"].named_steps["standardscaler"].n_samples_seen_,500)
        score=base["rbf_svm"].decision_function(x[parts["test"]])
        naive_sigmoid=1/(1+np.exp(-score))
        honest=calibrated["rbf_svm"].predict_proba(x[parts["test"]])[:,1]
        self.assertFalse(np.allclose(naive_sigmoid,honest))

    def test_calibrated_metrics_contract(self):
        r=self.result["heldout_comparison"]["test_calibrated_classifiers"]
        for name,expected in {"gaussian_nb":.44710928079248563,"knn":.47207135636048625,"rbf_svm":.4704766125497471}.items():
            self.assertAlmostEqual(r[name]["log_loss_nats"],expected,places=8)
            self.assertEqual(sum(r[name]["confusion_tn_fp_fn_tp"]),250)

class V1C12Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lab=load(12);cls.result=cls.lab.run()

    def test_gini_gain(self):
        r=self.result["split_fixture"]["gini"]
        assert_allclose([r[k] for k in ("parent","left","right","weighted_children","gain")],[.5,0,.375,.25,.25])

    def test_entropy_gain(self):
        r=self.result["split_fixture"]["entropy_bits"]
        self.assertAlmostEqual(r["gain"],1-(8/12)*(-.75*np.log2(.75)-.25*np.log2(.25)))
        self.assertAlmostEqual(r["gain"],.4591479170272448)

    def test_fitted_stump_matches_manual_partition(self):
        r=self.result["split_fixture"]
        self.assertEqual(r["fitted_stump_threshold"],.5);assert_allclose(r["fitted_stump_probabilities"],[0,.75])
        self.assertEqual(r["root_cost_at_tie"],r["stump_cost_at_tie"])

    def test_invalid_impurity_inputs(self):
        for p,n,criterion in [(-1,2,"gini"),(3,2,"gini"),(0,0,"gini"),(1,2,"unknown")]:
            with self.assertRaises(ValueError): self.lab.binary_impurity(p,n,criterion)
        self.assertEqual(self.lab.binary_impurity(0,4,"entropy"),0)
        self.assertEqual(self.lab.binary_impurity(4,4,"gini"),0)

    def test_boosting_residual_step(self):
        r=self.result["boosting_fixture"]
        self.assertEqual(r["initial_prediction"],6);assert_allclose(r["residuals"],[-4,-2,2,4])
        self.assertEqual(r["stump_threshold"],1.5);assert_allclose(r["stump_prediction"],[-3,-3,3,3])
        assert_allclose(r["updated_prediction"],[4.5,4.5,7.5,7.5])
        assert_allclose([r["initial_mse"],r["updated_mse"],r["eta_one_mse"]],[10,3.25,1])

    def test_ensemble_partition_and_refit_size(self):
        r=self.result["ensemble_comparison"];check_partition(self,r["split_indices"],800)
        self.assertEqual(r["split_sizes"],{"train":480,"validation":160,"test":160})
        self.assertEqual(r["refit_rows"],640)
        self.assertTrue(all(row["n"]==160 for row in r["test_scores"].values()))

    def test_selection_uses_validation_log_loss(self):
        r=self.result["ensemble_comparison"]
        expected=min(r["validation_scores"],key=lambda name:r["validation_scores"][name]["log_loss_nats"])
        self.assertEqual(r["selected_before_test"],expected)
        self.assertEqual(expected,"logistic_baseline")

    def test_models_are_modest_and_deterministic(self):
        models=self.lab.model_candidates()
        self.assertEqual(models["random_forest"].n_estimators,80)
        self.assertEqual(models["random_forest"].n_jobs,1)
        self.assertEqual(models["gradient_boosting"].random_state,1212)
        self.assertEqual(models["decision_tree"].min_samples_leaf,12)

    def test_fixed_synthetic_logistic_baseline_result(self):
        r=self.result["ensemble_comparison"]["test_scores"]
        self.assertAlmostEqual(r["logistic_baseline"]["log_loss_nats"],.44325827150706115,places=8)
        self.assertLess(r["logistic_baseline"]["log_loss_nats"],r["random_forest"]["log_loss_nats"])

class V1C13Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.lab=load(13);cls.result=cls.lab.run()

    def test_kmeans_centers_and_wcss(self):
        r=self.result["clustering_fixture"]
        assert_allclose(r["centers"],[[2/3,2/3],[26/3,26/3]])
        self.assertAlmostEqual(r["wcss"],32/3)
        self.assertAlmostEqual(sum(r["squared_distances_to_assigned_center"]),r["wcss"])

    def test_new_point_distances_and_one_center(self):
        r=self.result["clustering_fixture"]
        assert_allclose(r["new_point_squared_distances"],[2/9,1058/9])
        self.assertAlmostEqual(r["one_cluster_wcss"],608/3)

    def test_pca_sample_covariance_and_eigenvalues(self):
        r=self.result["pca_fixture"]
        assert_allclose(r["sample_covariance_ddof1"],np.full((2,2),10/3))
        assert_allclose(r["eigenvalues_descending"],[20/3,0]);assert_allclose(r["explained_variance_ratio"],[1,0])
        self.assertAlmostEqual(np.trace(r["sample_covariance_ddof1"]),sum(r["eigenvalues_descending"]))

    def test_pca_scores_and_sign_invariance(self):
        r=self.result["pca_fixture"];v=np.asarray(r["leading_eigenvector_canonical_sign"]);x=self.lab.PCA_POINTS
        assert_allclose(r["scores_canonical_sign"],np.sqrt(2)*np.array([-2,-1,1,2]))
        assert_allclose(np.outer(x@v,v),np.outer(x@(-v),-v))
        assert_allclose(r["rank_one_reconstruction"],x,atol=1e-14)
        self.assertLess(r["squared_reconstruction_error"],1e-25)

    def test_sklearn_and_numpy_pca_agree(self):
        r=self.result["pca_fixture"]
        self.assertAlmostEqual(r["sklearn_explained_variance"][0],r["eigenvalues_descending"][0])

    def test_unsupervised_train_test_partition(self):
        r=self.result["heldout_experiment"];check_partition(self,r["split_indices"],360)
        self.assertEqual(r["split_sizes"],{"train":270,"test":90})

    def test_unsupervised_scaler_pca_fitted_only_on_train(self):
        r=self.result["heldout_experiment"];x=self.lab.synthetic_activity();train=r["split_indices"]["train"]
        assert_allclose(r["training_scaler_mean"],x[train].mean(axis=0))
        assert_allclose(r["training_scaler_variance"],x[train].var(axis=0))
        self.assertEqual(r["scaler_n_samples_seen"],270);self.assertEqual(r["pca_n_training_samples"],270)

    def test_finite_geometry_not_business_segments(self):
        r=self.result["heldout_experiment"]
        self.assertEqual(sum(r["test_cluster_counts"]),90)
        self.assertTrue(-1<=r["test_silhouette"]<=1)
        self.assertGreaterEqual(r["test_pca_mse_per_standardized_coordinate"],0)
        self.assertLess(r["test_mean_squared_distance_k3"],r["test_mean_squared_distance_k1"])

class ClassicalCrossChapterTests(unittest.TestCase):
    def test_seeded_generator_reproducibility(self):
        a,b=classification_data(44,40);c,d=classification_data(44,40)
        assert_allclose(a,c);assert_allclose(b,d)
        e,f=classification_data(45,40);self.assertFalse(np.allclose(a,e))

    def test_invalid_split_fractions_rejected(self):
        for t,v in [(0,.2),(.8,.2),(.6,-.1)]:
            with self.assertRaises(ValueError): three_way_indices(np.array([0,1]*20),1,t,v)

    def test_metrics_match_direct_probability_arithmetic(self):
        y=np.array([0,1,0,1]);p=np.array([.1,.8,.4,.7]);r=binary_metrics(y,p)
        self.assertAlmostEqual(r["brier_score"],np.mean((y-p)**2))
        self.assertAlmostEqual(r["log_loss_nats"],-np.mean(y*np.log(p)+(1-y)*np.log1p(-p)))
        self.assertEqual(r["confusion_tn_fp_fn_tp"],[2,0,0,2])

    def test_metrics_reject_invalid_probability_or_class_inputs(self):
        for y,p in [([0,1],[np.nan,.5]),([0,1],[-.1,.7]),([0,1],[.5]),([1,1],[.1,.5])]:
            with self.assertRaises(ValueError): binary_metrics(y,p)

    def test_all_new_labs_repeat_without_result_drift(self):
        for number in range(9,14):
            lab=load(number)
            first=json.dumps(plain(lab.run()),sort_keys=True,allow_nan=False)
            second=json.dumps(plain(lab.run()),sort_keys=True,allow_nan=False)
            self.assertEqual(first,second)

if __name__ == "__main__": unittest.main()
