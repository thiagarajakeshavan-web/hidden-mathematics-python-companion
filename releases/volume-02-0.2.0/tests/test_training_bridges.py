"""Fresh algebraic oracles and edge cases; never read expected.json for mathematics."""
import copy
import math
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from volume2_companion import chapter15_optimizers as opt
from volume2_companion import chapter16_normalization as norm
from volume2_companion.registry import execute, verify, case_directory


class AdaptiveOptimizerTests(unittest.TestCase):
    def run_method(self, method, gradients=(2., -1.), **kwargs):
        return opt.trace(gradients, method, **kwargs)

    def test_adagrad_hand_updates(self):
        r=self.run_method('adagrad'); e=1e-8
        first=-.2/(2+e); second=first+.1/(math.sqrt(5)+e)
        self.assertAlmostEqual(r['steps'][0]['parameter'],first,places=14)
        self.assertAlmostEqual(r['final_parameter'],second,places=14)
        self.assertEqual([s['sum_squares'] for s in r['steps']],[4.,5.])

    def test_rmsprop_hand_updates(self):
        r=self.run_method('rmsprop'); e=1e-8
        first=-.2/(math.sqrt(2/5)+e)
        second=first+.1/(math.sqrt(23/50)+e)
        self.assertAlmostEqual(r['final_parameter'],second,places=14)
        self.assertAlmostEqual(r['steps'][1]['second_moment'],23/50,places=14)

    def test_adam_hand_bias_corrections(self):
        r=self.run_method('adam');s=r['steps'][1]
        self.assertAlmostEqual(s['first_moment'],2/25)
        self.assertAlmostEqual(s['second_moment'],23/50)
        self.assertAlmostEqual(s['corrected_first_moment'],8/19)
        self.assertAlmostEqual(s['corrected_second_moment'],46/19)
        wanted=-.2/(2+1e-8)-.1*(8/19)/(math.sqrt(46/19)+1e-8)
        self.assertAlmostEqual(r['final_parameter'],wanted,places=14)

    def test_adam_first_step_corrected(self):
        s=self.run_method('adam')['steps'][0]
        self.assertEqual(s['corrected_first_moment'],2.)
        self.assertEqual(s['corrected_second_moment'],4.)
        self.assertAlmostEqual(s['parameter_change'],-.1,places=8)

    def test_momentum_can_continue_after_gradient_reversal(self):
        r=self.run_method('adam')
        self.assertLess(r['steps'][1]['gradient'],0)
        self.assertLess(r['steps'][1]['parameter_change'],0)

    def test_epsilon_outside_root_all_methods(self):
        for method in ('adagrad','rmsprop','adam'):
            with self.subTest(method=method):
                r=self.run_method(method,[2.],epsilon=.25,beta1=0.,beta2=0.)
                self.assertAlmostEqual(r['final_parameter'],-.2/2.25)
                self.assertNotAlmostEqual(r['final_parameter'],-.2/math.sqrt(4.25))

    def test_zero_gradients_leave_parameter_unchanged(self):
        for method in ('adagrad','rmsprop','adam'):
            self.assertEqual(self.run_method(method,[0.,0.],initial_parameter=3.)['final_parameter'],3.)

    def test_zero_current_gradient_keeps_adam_history(self):
        self.assertLess(self.run_method('adam',[2.,0.])['steps'][1]['parameter_change'],0)
        self.assertEqual(self.run_method('rmsprop',[2.,0.])['steps'][1]['parameter_change'],0)

    def test_adagrad_accumulator_is_monotone(self):
        states=[s['sum_squares'] for s in self.run_method('adagrad',[1.,0.,-2.,3.])['steps']]
        self.assertEqual(states,[1.,1.,5.,14.])

    def test_rmsprop_forgets_past_squares(self):
        s=self.run_method('rmsprop',[2.,0.])['steps']
        self.assertAlmostEqual(s[1]['second_moment'],.9*s[0]['second_moment'])

    def test_adam_constant_gradient_corrected_moments(self):
        for s in self.run_method('adam',[3.]*12,beta1=.8,beta2=.95)['steps']:
            self.assertAlmostEqual(s['corrected_first_moment'],3.)
            self.assertAlmostEqual(s['corrected_second_moment'],9.)

    def test_invalid_epsilon(self):
        for v in (0,-1,float('nan'),float('inf'),True):
            with self.assertRaises(ValueError):self.run_method('adam',epsilon=v)

    def test_invalid_learning_rate(self):
        for v in (0,-1,float('nan'),float('inf'),True):
            with self.assertRaises(ValueError):self.run_method('adagrad',learning_rate=v)

    def test_invalid_beta(self):
        for k in ('beta1','beta2'):
            for v in (-.1,1.,float('nan'),float('inf'),True):
                with self.assertRaises(ValueError):self.run_method('adam',**{k:v})

    def test_invalid_gradients(self):
        for g in ([],[[1.]], [float('nan')],[float('inf')],[1e308]):
            with self.assertRaises(ValueError):self.run_method('adam',g)

    def test_nonfinite_parameter(self):
        with self.assertRaises(ValueError):self.run_method('adam',initial_parameter=float('inf'))

    def test_invalid_method(self):
        with self.assertRaises(ValueError):self.run_method('AdamW')

    def test_initial_parameter_translation(self):
        a=self.run_method('adam')['final_parameter']
        b=self.run_method('adam',initial_parameter=10.)['final_parameter']
        self.assertAlmostEqual(b-a,10.)

    def test_two_step_fixture_regression(self):
        self.assertEqual(verify(15,execute(15,2),2),[])


class NormalizationTests(unittest.TestCase):
    def setUp(self):
        self.args=dict(x=[[1.],[3.]],gamma=[2.],beta=[.5],epsilon=1e-5,
                       running_mean=[0.],running_variance=[1.],momentum=.1)
        self.infer=dict(x=[[1.],[3.]],gamma=[2.],beta=[.5],epsilon=1e-5,
                        running_mean=[1.],running_variance=[4.])

    def test_training_mean_variance_hand(self):
        r=norm.batch_norm_train(**self.args)
        np.testing.assert_array_equal(r['batch_mean'],[2.])
        np.testing.assert_array_equal(r['batch_variance_biased'],[1.])
        np.testing.assert_array_equal(r['batch_variance_unbiased'],[2.])

    def test_training_affine_hand(self):
        y=norm.batch_norm_train(**self.args)['output'].ravel()
        np.testing.assert_allclose(y,[.5-2/math.sqrt(1+1e-5),.5+2/math.sqrt(1+1e-5)],rtol=1e-14)

    def test_running_update_uses_unbiased_variance(self):
        r=norm.batch_norm_train(**self.args)
        np.testing.assert_allclose(r['updated_running_mean'],[.2])
        np.testing.assert_allclose(r['updated_running_variance'],[.9*1+.1*2])
        self.assertNotEqual(r['updated_running_variance'][0],1.)

    def test_inference_uses_frozen_statistics(self):
        r=norm.batch_norm_infer(**self.infer)
        np.testing.assert_allclose(r['output'].ravel(),[.5,.5+4/math.sqrt(4+1e-5)],rtol=1e-14)
        np.testing.assert_array_equal(r['mean_used'],[1.])
        np.testing.assert_array_equal(r['variance_used'],[4.])

    def test_train_inference_are_different(self):
        self.assertNotAlmostEqual(norm.batch_norm_train(**self.args)['output'][0,0],norm.batch_norm_infer(**self.infer)['output'][0,0])

    def test_inference_batch_companions_do_not_change_first_output(self):
        args=copy.deepcopy(self.infer);args['x']=[[1.],[999.]]
        self.assertEqual(norm.batch_norm_infer(**args)['output'][0,0],norm.batch_norm_infer(**self.infer)['output'][0,0])

    def test_training_batch_companions_change_first_output(self):
        args=copy.deepcopy(self.args);args['x']=[[1.],[3.],[9.]]
        self.assertNotAlmostEqual(norm.batch_norm_train(**args)['output'][0,0],norm.batch_norm_train(**self.args)['output'][0,0])

    def test_inputs_not_mutated(self):
        original=copy.deepcopy(self.args);norm.batch_norm_train(**self.args)
        self.assertEqual(self.args,original)
        original=copy.deepcopy(self.infer);norm.batch_norm_infer(**self.infer)
        self.assertEqual(self.infer,original)

    def test_epsilon_is_inside_root(self):
        args=copy.deepcopy(self.args);args['epsilon']=.25
        y=norm.batch_norm_train(**args)['output'][1,0]
        self.assertAlmostEqual(y,.5+2/math.sqrt(1.25))
        self.assertNotAlmostEqual(y,.5+2/1.25)

    def test_constant_batch_returns_beta(self):
        args=copy.deepcopy(self.args);args['x']=[[2.],[2.]]
        r=norm.batch_norm_train(**args)
        np.testing.assert_array_equal(r['output'],[[.5],[.5]])
        np.testing.assert_array_equal(r['batch_variance_biased'],[0.])

    def test_one_sample_inference_allowed(self):
        args=copy.deepcopy(self.infer);args['x']=[[1.]]
        self.assertEqual(norm.batch_norm_infer(**args)['output'][0,0],.5)

    def test_one_sample_training_rejected_for_running_variance(self):
        args=copy.deepcopy(self.args);args['x']=[[1.]]
        with self.assertRaises(ValueError):norm.batch_norm_train(**args)

    def test_zero_running_variance_still_finite(self):
        args=copy.deepcopy(self.infer);args['running_variance']=[0.]
        self.assertTrue(np.all(np.isfinite(norm.batch_norm_infer(**args)['output'])))

    def test_negative_running_variance_rejected(self):
        args=copy.deepcopy(self.infer);args['running_variance']=[-1.]
        with self.assertRaises(ValueError):norm.batch_norm_infer(**args)

    def test_invalid_momentum(self):
        for value in (-.01,1.01,float('nan'),True):
            args=copy.deepcopy(self.args);args['momentum']=value
            with self.assertRaises(ValueError):norm.batch_norm_train(**args)

    def test_momentum_endpoints(self):
        args=copy.deepcopy(self.args);args['momentum']=0
        r=norm.batch_norm_train(**args)
        np.testing.assert_array_equal(r['updated_running_mean'],[0.]);np.testing.assert_array_equal(r['updated_running_variance'],[1.])
        args['momentum']=1;r=norm.batch_norm_train(**args)
        np.testing.assert_array_equal(r['updated_running_mean'],[2.]);np.testing.assert_array_equal(r['updated_running_variance'],[2.])

    def test_invalid_dimensions(self):
        for key,value in [('x',[]),('x',[1.,3.]),('x',[[float('nan')],[3.]]),('gamma',[1.,2.]),('beta',[]),('running_mean',[1.,2.])]:
            args=copy.deepcopy(self.args);args[key]=value
            with self.assertRaises(ValueError):norm.batch_norm_train(**args)

    def test_invalid_epsilon(self):
        for value in (0,-1,float('nan'),float('inf'),True):
            args=copy.deepcopy(self.args);args['epsilon']=value
            with self.assertRaises(ValueError):norm.batch_norm_train(**args)

    def test_extreme_overflow_rejected(self):
        args=copy.deepcopy(self.args);args['x']=[[1e308],[-1e308]]
        with self.assertRaises(ValueError):norm.batch_norm_train(**args)

    def test_normalized_variance_less_than_one_with_epsilon(self):
        z=norm.batch_norm_train(**self.args)['normalized'].ravel()
        self.assertAlmostEqual(float(np.mean(z*z)),1/(1+1e-5))
        self.assertLess(float(np.mean(z*z)),1.)

    def test_layer_norm_axis_hand_oracle(self):
        r=norm.layer_norm([[1.,3.],[5.,7.]],[1.,1.],[0.,0.],1e-5)
        np.testing.assert_array_equal(r['row_mean'],[[2.],[6.]])
        np.testing.assert_array_equal(r['row_variance_biased'],[[1.],[1.]])
        z=1/math.sqrt(1+1e-5)
        np.testing.assert_allclose(r['output'],[[-z,z],[-z,z]],rtol=1e-14)

    def test_batch_norm_column_axis_hand_oracle(self):
        r=norm.batch_norm_train([[1.,3.],[5.,7.]],[1.,1.],[0.,0.],1e-5,[0.,0.],[1.,1.],.1)
        np.testing.assert_array_equal(r['batch_mean'],[3.,5.])
        np.testing.assert_array_equal(r['batch_variance_biased'],[4.,4.])
        z=2/math.sqrt(4+1e-5)
        np.testing.assert_allclose(r['output'],[[-z,-z],[z,z]],rtol=1e-14)

    def test_layer_norm_single_feature_returns_beta(self):
        r=norm.layer_norm([[1.],[3.]],[2.],[.5],1e-5)
        np.testing.assert_array_equal(r['output'],[[.5],[.5]])

    def test_layer_norm_independent_of_other_rows(self):
        a=norm.layer_norm([[1.,3.],[5.,7.]],[1.,1.],[0.,0.],1e-5)
        b=norm.layer_norm([[1.,3.],[-100.,999.]],[1.,1.],[0.,0.],1e-5)
        np.testing.assert_array_equal(a['output'][0],b['output'][0])

    def test_case_regression(self):self.assertEqual(verify(16,execute(16,2),2),[])

    def test_unknown_case_rejected(self):
        with self.assertRaises(ValueError):case_directory(17,2)


if __name__=='__main__':unittest.main()
