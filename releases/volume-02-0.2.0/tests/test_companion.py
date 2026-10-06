"""Independent invariants, analytic oracles, negative cases and regression fixtures."""
import copy
import math
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from volume2_companion import numerics as n
from volume2_companion import chapter15 as c15, chapter16 as c16, chapter17 as c17
from volume2_companion import chapter18 as c18, chapter19 as c19, chapter20 as c20
from volume2_companion import chapter21 as c21, chapter22 as c22, chapter23 as c23
from volume2_companion import chapter24 as c24, chapter25 as c25, chapter26 as c26
from volume2_companion.registry import execute, verify, load_inputs, differences


def fixture(chapter):
    return copy.deepcopy(load_inputs(chapter)["inputs"])


class NumericTests(unittest.TestCase):
    def test_sigmoid_zero(self): self.assertEqual(n.sigmoid(0), .5)
    def test_sigmoid_extremes(self): self.assertEqual((n.sigmoid(-1000), n.sigmoid(1000)), (0, 1))
    def test_softplus_extremes(self): self.assertEqual((n.softplus(-1000), n.softplus(1000)), (0, 1000))
    def test_softmax_shift_invariance(self): np.testing.assert_allclose(n.softmax([1,2,3]), n.softmax([1001,1002,1003]))
    def test_softmax_large(self): np.testing.assert_allclose(n.softmax([10000,10000]), [.5,.5])
    def test_mask_exact_zero(self): self.assertEqual(n.softmax([1,1], [True,False])[1], 0)
    def test_all_masked_rejected(self): self.assertRaises(ValueError, n.softmax, [[0,0]], [[False,False]])
    def test_bad_mask_shape(self): self.assertRaises(ValueError, n.softmax, [0,0], [True])
    def test_nonfinite(self): self.assertRaises(ValueError, n.array, [1,np.nan])
    def test_log_softmax_extremes(self): np.testing.assert_allclose(n.log_softmax([1000,-1000]),[0,-2000])
    def test_softmax_scalar_rejected(self): self.assertRaises(ValueError,n.softmax,1)
    def test_softplus_nonfinite(self): self.assertRaises(ValueError,n.softplus,float("nan"))
    def test_empty(self): self.assertRaises(ValueError, n.array, [])
    def test_bad_dimension(self): self.assertRaises(ValueError, n.array, [[1]], 1)
    def test_bad_distribution(self): self.assertRaises(ValueError, n.probabilities, [.2,.2])
    def test_negative_probability(self): self.assertRaises(ValueError, n.probabilities, [-.1,1.1])
    def test_central_quadratic(self): np.testing.assert_allclose(n.central_gradient(lambda x: x@x, [1,2]), [2,4], atol=1e-8)
    def test_epsilon_zero_rejected(self): self.assertRaises(ValueError, n.central_gradient, lambda x:x@x, [1], 0)


class NeuralTests(unittest.TestCase):
    def setUp(self): self.i=fixture(15);self.t=np.array([.2,-.1,.3,.4,-.2]);self.x=np.array([1,2])
    def test_exact_pre_activation(self): self.assertAlmostEqual(c15.forward(self.t,self.x,1)['a'], -.08)
    def test_independent_bce(self): self.assertAlmostEqual(c15.forward(self.t,self.x,1)['loss'], -math.log(n.sigmoid(-.08)))
    def test_gradient_chain_rule(self): np.testing.assert_allclose(c15.gradient(self.t,self.x,1), (n.sigmoid(-.08)-1)*np.array([.4,.8,.4,.3,1]))
    def test_finite_difference(self): self.assertLess(c15.run(self.i)['max_gradient_error'], 1e-7)
    def test_one_step_decreases_this_loss(self): r=c15.run(self.i);self.assertLess(r['updated_loss'],r['loss'])
    def test_negative_relu(self): t=self.t.copy();t[2]=-1;np.testing.assert_allclose(c15.gradient(t,self.x,1)[:4],0)
    def test_kink_derivative_convention(self): t=self.t.copy();t[2]=0;np.testing.assert_allclose(c15.gradient(t,self.x,1)[:4],0)
    def test_zero_target_gradient_sign(self): self.assertGreater(c15.gradient(self.t,self.x,0)[-1],0)
    def test_invalid_target(self): self.assertRaises(ValueError,c15.forward,self.t,self.x,.5)
    def test_mismatched_features(self): self.assertRaises(ValueError,c15.forward,self.t,[1],1)
    def test_large_logit_loss_finite(self): t=self.t.copy();t[-1]=1000;self.assertTrue(math.isfinite(c15.forward(t,self.x,0)['loss']))
    def test_simultaneous_update(self): r=c15.run(self.i);np.testing.assert_allclose(r['updated_parameters'],self.t-.1*c15.gradient(self.t,self.x,1))
    def test_seeded_gradient_sweep(self):
        rng=np.random.default_rng(15)
        for _ in range(25):
            x=rng.normal(size=2);t=rng.normal(size=5);t[2]=abs(t[:2]@x)+1
            np.testing.assert_allclose(c15.gradient(t,x,1),n.central_gradient(lambda p:c15.forward(p,x,1)['loss'],t),atol=1e-7)


class ArchitectureTests(unittest.TestCase):
    def test_correlation_not_convolution(self): np.testing.assert_array_equal(c16.cross_correlation([2,3,5,4],[1,-1]),[-1,-2,1])
    def test_stride(self): np.testing.assert_array_equal(c16.cross_correlation([1,2,3,4],[1,1],2),[3,7])
    def test_padding(self): np.testing.assert_array_equal(c16.cross_correlation([1,2],[1,1],1,1),[1,3,2])
    def test_stride_zero(self): self.assertRaises(ValueError,c16.cross_correlation,[1,2],[1],0)
    def test_padding_negative(self): self.assertRaises(ValueError,c16.cross_correlation,[1,2],[1],1,-1)
    def test_kernel_too_long(self): self.assertRaises(ValueError,c16.cross_correlation,[1],[1,2])
    def test_rnn_zero_sequence(self): np.testing.assert_array_equal(c16.rnn([0,0],.5,.5,0),[0,0])
    def test_rnn_second_step(self): self.assertAlmostEqual(c16.rnn([1,0],.5,.5,0)[1],math.tanh(.5*math.tanh(.5)))
    def test_rnn_hidden_bounded(self): self.assertLessEqual(abs(c16.rnn([1e4,-1e4],1,1,0)).max(),1)
    def test_lstm_cell(self): self.assertAlmostEqual(c16.lstm_cell(.8,.75,.25,.4,.5)[0],.7)
    def test_lstm_closed_output(self): self.assertEqual(c16.lstm_cell(2,1,0,0,0),(2,0))
    def test_lstm_invalid_gate(self): self.assertRaises(ValueError,c16.lstm_cell,.8,1.1,.25,.4,.5)
    def test_lstm_invalid_candidate(self): self.assertRaises(ValueError,c16.lstm_cell,.8,.75,.25,1.1,.5)
    def test_direct_carry(self): self.assertGreater(c16.run(fixture(16))['ten_step_carry_099'],c16.run(fixture(16))['ten_step_carry_075'])


class AttentionTests(unittest.TestCase):
    def setUp(self): self.i=fixture(17)
    def test_scores_scale(self): self.assertAlmostEqual(c17.run(self.i)['scores'][0,0],1/math.sqrt(2))
    def test_mask_rows_sum_one(self): np.testing.assert_allclose(c17.run(self.i)['causal_weights'].sum(axis=1),1)
    def test_future_is_zero(self): self.assertEqual(c17.run(self.i)['causal_weights'][0,1],0)
    def test_first_token_cannot_see_future_value(self): i=fixture(17);i['V'][1]=[1e6,1e6];np.testing.assert_allclose(c17.run(i)['causal_output'][0],[2,0])
    def test_second_token_weight(self): self.assertAlmostEqual(c17.run(self.i)['causal_weights'][1,1],1/(1+math.exp(-1/math.sqrt(2))))
    def test_output_dimensions(self): self.assertEqual(c17.attention([[1,0]],[[0,1]],[[1,2,3]])[2].shape,(1,3))
    def test_qk_dimension_mismatch(self): self.assertRaises(ValueError,c17.attention,[[1]],[[1,0]],[[1]])
    def test_kv_tokens_mismatch(self): self.assertRaises(ValueError,c17.attention,[[1]],[[1]],[[1],[2]])
    def test_causal_length_mismatch(self): self.assertRaises(ValueError,c17.attention,[[1]],[[1],[2]],[[1],[2]])
    def test_unmasked_cross_attention(self): self.assertEqual(c17.attention([[1]],[[1],[2]],[[1],[2]],False)[2].shape,(1,1))
    def test_position_zero(self): np.testing.assert_array_equal(c17.sinusoidal([0],4),[[0,1,0,1]])
    def test_odd_position_dimension(self): self.assertRaises(ValueError,c17.sinusoidal,[0],3)
    def test_position_pair_norm(self): p=c17.sinusoidal([0,1,100],4);np.testing.assert_allclose(p[:,0::2]**2+p[:,1::2]**2,1)


class LanguageModelTests(unittest.TestCase):
    def setUp(self): self.i=fixture(18)
    def test_merge_output(self): self.assertEqual(c18.run(self.i)['merge_stages'][-1],['milk</w>'])
    def test_no_eligible_merge(self): self.assertEqual(c18.merge_symbols(['a','b'],[['x','y']]),[['a','b']])
    def test_overlapping_pairs(self): self.assertEqual(c18.merge_symbols(['a','a','a'],[['a','a']])[-1],['aa','a'])
    def test_rank_priority(self): self.assertEqual(c18.merge_symbols(['a','b','c'],[['b','c'],['a','b']])[-1],['a','bc'])
    def test_duplicate_merge_rejected(self): self.assertRaises(ValueError,c18.merge_symbols,['a','b'],[['a','b'],['a','b']])
    def test_probabilities_exact(self): np.testing.assert_array_equal(c18.run(self.i)['conditional_probabilities'],[.5,.25,.125,.125])
    def test_zero_counts_uniform(self): np.testing.assert_allclose(c18.conditional_counts(['a','b'],[0,0]),[.5,.5])
    def test_negative_counts(self): self.assertRaises(ValueError,c18.conditional_counts,['a','b'],[-1,1])
    def test_fractional_counts(self): self.assertRaises(ValueError,c18.conditional_counts,['a','b'],[.5,1])
    def test_zero_smoothing(self): self.assertRaises(ValueError,c18.conditional_counts,['a'],[1],0)
    def test_unknown_target(self): self.assertRaises(ValueError,c18.negative_log_likelihood,['a'],[1],['b'])
    def test_perplexity(self): self.assertAlmostEqual(c18.run(self.i)['perplexity'],4)
    def test_scaling_exponent(self): self.assertAlmostEqual(c18.run(self.i)['synthetic_power_exponent'],.5)
    def test_scaling_floor_violation(self): self.assertRaises(ValueError,c18.scaling_fit,[[1,1],[2,2]],1)
    def test_nll_bad_distribution(self): self.assertRaises(ValueError,c18.negative_log_likelihood,["a","b"],[.2,.2],["a"])
    def test_scaling_nan_floor(self): self.assertRaises(ValueError,c18.scaling_fit,[[1,2],[4,1.5]],float("nan"))
    def test_duplicate_compute(self): self.assertRaises(ValueError,c18.scaling_fit,[[1,2],[1,3]],1)


class AlignmentTests(unittest.TestCase):
    def setUp(self): self.i=fixture(19)
    def test_sft_gradient(self): np.testing.assert_allclose(c19.run(self.i)['sft']['gradient'],[-.5,.5])
    def test_sft_gradient_sum_zero(self): self.assertAlmostEqual(float(c19.sft_step([1,2,3],1,.1)['gradient'].sum()),0)
    def test_sft_decrease(self): r=c19.run(self.i)['sft'];self.assertLess(r['loss_after'],r['loss_before'])
    def test_sft_invalid_index(self): self.assertRaises(ValueError,c19.sft_step,[0,0],2,.1)
    def test_sft_large_logit(self): self.assertTrue(math.isfinite(c19.sft_step([1000,-1000],1,.1)['loss_before']))
    def test_dpo_neutral_reference(self): self.assertAlmostEqual(c19.dpo(.4,.4,.4,.4,.5)['loss'],math.log(2))
    def test_dpo_uses_reference(self): self.assertAlmostEqual(c19.dpo(.6,.2,.6,.2,.5)['margin'],0)
    def test_dpo_gradient(self): self.assertLess(c19.run(self.i)['dpo']['max_gradient_error'],1e-7)
    def test_dpo_zero_probability(self): self.assertRaises(ValueError,c19.dpo,0,.2,.4,.4,.5)
    def test_dpo_invalid_distribution(self): self.assertRaises(ValueError,c19.dpo,.8,.8,.4,.4,.5)
    def test_dpo_tiny_nonzero_probabilities(self): self.assertTrue(math.isfinite(c19.dpo(.5,1e-320,.4,.4,.5)["loss"]))
    def test_dpo_beta(self): self.assertRaises(ValueError,c19.dpo,.6,.2,.4,.4,0)
    def test_lora_adds_to_base(self): np.testing.assert_allclose(c19.run(self.i)['lora']['combined_output'],[4.1,10.2])
    def test_lora_zero_B(self): np.testing.assert_allclose(c19.lora([[1,2],[3,4]],[[1,-1]],[[0],[0]],[2,1])['combined_output'],[4,10])
    def test_lora_dimension_mismatch(self): self.assertRaises(ValueError,c19.lora,[[1]],[[1,2]],[[1]],[1])
    def test_lora_does_not_mutate(self): w=np.eye(2);c19.lora(w,[[1,1]],[[1],[1]],[1,1]);np.testing.assert_array_equal(w,np.eye(2))


class RetrievalTests(unittest.TestCase):
    def test_cosine_identical(self): self.assertAlmostEqual(c20.cosine([1,1],[1,1]),1)
    def test_cosine_orthogonal(self): self.assertEqual(c20.cosine([1,0],[0,1]),0)
    def test_zero_vector_rejected(self): self.assertRaises(ValueError,c20.cosine,[1,0],[0,0])
    def test_large_finite_vectors(self): self.assertAlmostEqual(c20.cosine([1e200,1e200],[1e200,1e200]),1)
    def test_subnormal_vectors(self): self.assertAlmostEqual(c20.cosine([1e-320,1e-320],[1e-320,1e-320]),1)
    def test_dimension_mismatch(self): self.assertRaises(ValueError,c20.cosine,[1],[1,2])
    def test_auth_freshness_before_rank(self): self.assertEqual([r['id'] for r in c20.run(fixture(20))['ranked_authorized_current']],['D1','D2'])
    def test_unauthorized_malformed_not_scored(self): self.assertEqual(c20.retrieve([1],[{'authorized':False,'vector':'private malformed'}]),[])
    def test_string_permission_not_authority(self): self.assertEqual(c20.retrieve([1],[{'authorized':'true','current':True}]),[])
    def test_missing_permission_denies(self): self.assertEqual(c20.retrieve([1],[{'current':True}]),[])
    def test_restriction_not_score(self): self.assertEqual(c20.run(fixture(20))['restriction_review_candidate_ids'],['D2'])
    def test_deterministic_tie(self): docs=[{'id':x,'authorized':True,'current':True,'vector':[1]} for x in ['B','A']];self.assertEqual([r['id'] for r in c20.retrieve([1],docs)],['A','B'])


class AgentTests(unittest.TestCase):
    def setUp(self): self.i=fixture(21)
    def test_quote_total(self): self.assertEqual(c21.simulate(self.i)['quote_total_aud'],'36.50')
    def test_calls_bounded(self): self.assertEqual(c21.simulate(self.i)['tool_call_count'],3)
    def test_purchase_denied(self): self.assertEqual(c21.simulate(self.i,attempted_action='purchase')['status'],'denied')
    def test_calculator_requires_validated_catalogue(self): self.assertEqual(c21.simulate(self.i,attempted_action='calculate_total')['status'],'denied')
    def test_arbitrary_write_denied(self): self.assertEqual(c21.simulate(self.i,attempted_action='delete_profile')['tool_call_count'],0)
    def test_unknown_evidence_blocks(self): self.assertEqual(c21.simulate(self.i,evidence='missing')['status'],'blocked_unknown_restriction')
    def test_cross_contact_blocks(self): self.assertIsNone(c21.simulate(self.i,evidence='cross_contact_unresolved')['quote_total_aud'])
    def test_injection_no_authority(self): r=c21.simulate(self.i,injected=True);self.assertFalse(r['purchase_executed']);self.assertNotIn('purchase',r['tool_calls'])
    def test_budget_zero(self): self.assertEqual(c21.simulate(self.i,max_tool_calls=0)['tool_call_count'],0)
    def test_budget_two(self): self.assertEqual(c21.simulate(self.i,max_tool_calls=2)['status'],'budget_exhausted')
    def test_negative_call_limit(self): self.assertRaises(ValueError,c21.simulate,self.i,max_tool_calls=-1)
    def test_over_financial_budget(self): self.i['budget_aud']=35;self.assertEqual(c21.simulate(self.i)['status'],'infeasible_budget')
    def test_exact_financial_budget(self): self.i['budget_aud']=36.5;self.assertEqual(c21.simulate(self.i)['status'],'ready_for_review')
    def test_negative_price(self): self.assertRaises(ValueError,c21.money,-1)
    def test_nan_price(self): self.assertRaises(ValueError,c21.money,'NaN')
    def test_allowlist_cannot_expand(self): self.i['read_tools'].append('purchase');self.assertRaises(ValueError,c21.simulate,self.i)


class DataEngineeringTests(unittest.TestCase):
    def setUp(self): self.i=fixture(22)
    def test_known_at_prevents_leakage(self): self.assertEqual(c22.run(self.i)['at_1000']['price_aud'],12)
    def test_late_available_selects(self): self.assertEqual(c22.run(self.i)['at_1015']['price_aud'],10)
    def test_future_conflict_not_historical_knowledge(self):
        rs=self.i['records']+[{**self.i['records'][0],'available_at':'2026-10-06T10:30:00Z','price_aud':99}]
        r=c22.as_of(rs,self.i['decision_time'],24,self.i['entity'],self.i['entity'])
        self.assertEqual(r['price_aud'],12);self.assertEqual(r['quarantined_ids'],[])
    def test_other_entity_conflict_does_not_quarantine(self):
        rs=self.i['records']+[{**self.i['records'][0],'entity':'P2','price_aud':99}]
        r=c22.as_of(rs,self.i['decision_time'],24,self.i['entity'],self.i['entity'])
        self.assertEqual(r['price_aud'],12)
    def test_missing_entity(self): self.assertIsNone(c22.run(self.i)['missing_entity']['price_aud'])
    def test_stale(self): self.assertIsNone(c22.run(self.i)['all_stale']['price_aud'])
    def test_deduplicate_identical(self): self.assertEqual(len(c22.deduplicate(self.i['records'])[0]),3)
    def test_conflict_quarantine(self): self.assertEqual(c22.run(self.i)['conflicting_duplicate']['quarantined_ids'],['P1-a'])
    def test_conflict_order_independent(self): rs=self.i['records']+[{**self.i['records'][0],'price_aud':99}];self.assertEqual(c22.deduplicate(rs)[1],c22.deduplicate(list(reversed(rs)))[1])
    def test_ttl_boundary_inclusive(self): r=c22.as_of([self.i['records'][0]],'2026-10-06T12:00:00Z',24,self.i['entity'],self.i['entity']);self.assertEqual(r['selected_id'],'P1-a')
    def test_just_beyond_ttl_is_stale(self): r=c22.as_of([self.i['records'][0]],'2026-10-06T12:00:01Z',24,self.i['entity'],self.i['entity']);self.assertIsNone(r['selected_id'])
    def test_availability_time_boundary(self): r=c22.as_of(self.i['records'],'2026-10-06T10:10:00Z',24,self.i['entity'],self.i['entity']);self.assertEqual(r['selected_id'],'P1-b')
    def test_naive_timestamp_rejected(self): self.assertRaises(ValueError,c22.timestamp,'2026-10-06T10:00:00')
    def test_timezone_equivalence(self): self.assertEqual(c22.timestamp('2026-10-06T10:00:00Z'),c22.timestamp('2026-10-06T12:00:00+02:00'))
    def test_negative_ttl(self): self.assertRaises(ValueError,c22.as_of,[],self.i['decision_time'],-1,'x')
    def test_negative_record_price(self): r={**self.i['records'][0],'price_aud':-1};self.assertRaises(ValueError,c22.deduplicate,[r])
    def test_future_event_excluded(self): r=c22.as_of([self.i['records'][2]],self.i['decision_time'],24,self.i['entity'],self.i['entity']);self.assertIsNone(r['selected_id'])


class EvaluationTests(unittest.TestCase):
    def test_detector_orientation(self): r=c23.run(fixture(23))['unsupported_detector'];self.assertEqual([r[k] for k in ['tp','fp','fn','tn']],[2,1,1,6])
    def test_no_predicted_positive(self): self.assertIsNone(c23.confusion([0,1],[0,0])['precision'])
    def test_no_actual_positive(self): self.assertIsNone(c23.confusion([0,0],[0,1])['recall'])
    def test_labels_must_binary(self): self.assertRaises(ValueError,c23.confusion,[0,2],[0,1])
    def test_shape_mismatch(self): self.assertRaises(ValueError,c23.confusion,[1],[1,0])
    def test_brier(self): self.assertAlmostEqual(c23.run(fixture(23))['brier'],.175)
    def test_one_bin_misleading(self): self.assertAlmostEqual(c23.run(fixture(23))['ece_one_bin'],0)
    def test_one_bin_membership(self): self.assertEqual(c23.run(fixture(23))["one_bin_membership"],[0,1,2,3])
    def test_confidence_range(self): self.assertRaises(ValueError,c23.calibration,[1.1],[1])
    def test_wilson_contains_estimate(self): lo,hi=c23.wilson(7,10);self.assertLess(lo,.7);self.assertGreater(hi,.7)
    def test_wilson_zero_all(self): self.assertAlmostEqual(c23.wilson(0,10)[0],0);self.assertAlmostEqual(c23.wilson(10,10)[1],1)
    def test_wilson_no_samples(self): self.assertRaises(ValueError,c23.wilson,0,0)
    def test_bootstrap_deterministic(self): a=c23.run(fixture(23));b=c23.run(fixture(23));np.testing.assert_array_equal(a['paired_bootstrap_95_percentile_interval'],b['paired_bootstrap_95_percentile_interval'])
    def test_bootstrap_identical_pairs(self): r=c23.paired_bootstrap([0,1],[0,1],23,100);np.testing.assert_array_equal(r['paired_bootstrap_95_percentile_interval'],[0,0])
    def test_bootstrap_replicates_invalid(self): self.assertRaises(ValueError,c23.paired_bootstrap,[0],[1],1,0)
    def test_retrieval_denominator_invalid(self): i=fixture(23);i['total_relevant']=2;self.assertRaises(ValueError,c23.run,i)


class EfficiencyTests(unittest.TestCase):
    def test_quantized_ints(self): np.testing.assert_array_equal(c24.quantize([-1,-.5,0,.5,1])['integers'],[-127,-64,0,64,127])
    def test_quantization_error_bound(self): r=c24.quantize(np.linspace(-3,3,41));self.assertLessEqual(r['max_absolute_error'],r['scale']/2+1e-12)
    def test_all_zero_quantization(self): r=c24.quantize([0,0]);self.assertEqual(r['scale'],1);self.assertEqual(r['max_absolute_error'],0)
    def test_quantizer_dtype(self): self.assertEqual(c24.quantize([1])['integers'].dtype,np.int8)
    def test_unrepresentable_quantization_scale_rejected(self): self.assertRaises(ValueError,c24.quantize,[float.fromhex("0x0.0000000000001p-1022")])
    def test_qmax_invalid(self): self.assertRaises(ValueError,c24.quantize,[1],128)
    def test_prune_threshold_boundary(self): np.testing.assert_array_equal(c24.prune([.05,.049,-.05],.05)['pruned'],[.05,0,-.05])
    def test_prune_negative_threshold(self): self.assertRaises(ValueError,c24.prune,[1],-1)
    def test_kl_identical(self): self.assertAlmostEqual(c24.kl_divergence([.3,.7],[.3,.7]),0)
    def test_kl_zero_teacher_mass(self): self.assertAlmostEqual(c24.kl_divergence([1,0],[.5,.5]),math.log(2))
    def test_kl_tiny_student_mass_finite(self): self.assertTrue(math.isfinite(c24.kl_divergence([.5,.5],[1e-320,1.])))
    def test_kl_missing_support(self): self.assertRaises(ValueError,c24.kl_divergence,[.5,.5],[1,0])
    def test_distillation_actual_updates(self): r=c24.distill([.7,.2,.1],[.6,.25,.15]);self.assertLess(r['kl_after'],r['kl_before'])
    def test_distillation_trajectory(self): r=c24.distill([.7,.2,.1],[.6,.25,.15]);self.assertTrue(np.all(np.diff(r['kl_trajectory'])<0))
    def test_distillation_gradient_central_difference(self): self.assertLess(c24.distill([.7,.2,.1],[.6,.25,.15])["gradient_check"]["max_gradient_error"],1e-7)
    def test_pruning_mask(self): np.testing.assert_array_equal(c24.prune([.05,.049,-.05],.05)["pruning_keep_mask"],[True,False,True])
    def test_distillation_zero_steps(self): r=c24.distill([.7,.2,.1],[.6,.25,.15],0);self.assertEqual(r['kl_before'],r['kl_after'])
    def test_kv_bytes(self): self.assertEqual(c24.run(fixture(24))['kv_bytes'],2*12*1*2048*8*64*2)
    def test_weight_storage_excludes_runtime(self): r=c24.run(fixture(24));self.assertEqual(r['int8_tensor_bytes_with_scale'],1000004)


class SafetyTests(unittest.TestCase):
    def test_allow_exact_trusted_fixture(self): p=fixture(25)['policy_cases'][0];self.assertEqual(c25.policy(p),'allow')
    def test_denial_reasons(self): p=fixture(25)["policy_cases"][3];self.assertEqual(c25.policy_reasons(p),["invalid_arguments"])
    def test_missing_auth_denied(self): p=fixture(25)['policy_cases'][0];del p['trusted_user_authorized'];self.assertEqual(c25.policy(p),'deny')
    def test_string_auth_denied(self): p=fixture(25)['policy_cases'][0];p['trusted_user_authorized']='true';self.assertEqual(c25.policy(p),'deny')
    def test_sensitive_export_denied(self): p=fixture(25)['policy_cases'][0];p['sensitive_export']=True;self.assertEqual(c25.policy(p),'deny')
    def test_unknown_action_denied(self): p=fixture(25)['policy_cases'][0];p['action']='admin';self.assertEqual(c25.policy(p),'deny')
    def test_invalid_args_denied(self): p=fixture(25)['policy_cases'][0];p['arguments_valid']=False;self.assertEqual(c25.policy(p),'deny')
    def test_abstract_fairness_rates(self): self.assertEqual(c25.cohort_metrics(fixture(25)['group_a']),{'tpr':.8,'fpr':.2,'accuracy':.8,'size':20})
    def test_undefined_fairness_denominator(self): self.assertIsNone(c25.cohort_metrics({'tp':0,'fn':0,'fp':1,'tn':1})['tpr'])
    def test_negative_confusion_count(self): self.assertRaises(ValueError,c25.cohort_metrics,{'tp':-1,'fn':1,'fp':1,'tn':1})
    def test_noninteger_confusion_count(self): self.assertRaises(ValueError,c25.cohort_metrics,{'tp':1.5,'fn':1,'fp':1,'tn':1})
    def test_unknown_evidence_conservative(self): self.assertEqual(c25.evidence_gate('unrecognized'),'withhold')
    def test_known_evidence_only_review(self): self.assertEqual(c25.evidence_gate('current_resolved'),'review_eligible')
    def test_ascii_email_redacted(self): self.assertEqual(c25.redact_ascii_email('x@example.test'),'[EMAIL]')
    def test_redaction_not_general_pii(self): self.assertEqual(c25.redact_ascii_email('Synthetic ID 12345'),'Synthetic ID 12345')


class OperationsTests(unittest.TestCase):
    def test_drift_distance(self): self.assertAlmostEqual(c26.total_variation([.6,.3,.1],[.4,.4,.2]),.2)
    def test_no_drift(self): self.assertEqual(c26.total_variation([.6,.4],[.6,.4]),0)
    def test_disjoint_distributions(self): self.assertEqual(c26.total_variation([1,0],[0,1]),1)
    def test_drift_bins_mismatch(self): self.assertRaises(ValueError,c26.total_variation,[1],[.5,.5])
    def test_invalid_distribution(self): self.assertRaises(ValueError,c26.total_variation,[.1,.1],[.5,.5])
    def test_error_budget(self): r=c26.error_budget(10000,30,.995);self.assertEqual(r['allowed_bad_requests'],50);self.assertEqual(r['remaining_budget'],20)
    def test_budget_exhausted_can_negative(self): self.assertLess(c26.error_budget(10000,60,.995)['remaining_budget'],0)
    def test_zero_requests_undefined(self): self.assertRaises(ValueError,c26.error_budget,0,0,.99)
    def test_bad_exceeds_total(self): self.assertRaises(ValueError,c26.error_budget,10,11,.99)
    def test_perfect_target_rejected(self): self.assertRaises(ValueError,c26.error_budget,10,0,1)
    def test_little_units(self): self.assertEqual(c26.run(fixture(26))['mean_concurrency'],4)
    def test_speedup_full_path(self): self.assertAlmostEqual(c26.run(fixture(26))['speedup'],110/70)
    def test_nearest_rank(self): self.assertEqual(c26.nearest_rank([1,2,3,4,5],.95),5)
    def test_negative_latency(self): self.assertRaises(ValueError,c26.nearest_rank,[1,-1],.5)


class ReproducibilityTests(unittest.TestCase):
    def test_all_cases_match_recorded_results(self):
        for chapter in range(15,27):
            with self.subTest(chapter=chapter): self.assertEqual(verify(chapter,execute(chapter)),[])
    def test_bool_not_numeric(self): self.assertTrue(differences(1,True))
    def test_missing_keys_fail(self): self.assertTrue(differences({}, {'x':1}))
    def test_tolerance_float(self): self.assertEqual(differences(.1+.2,.3),[])
    def test_nan_does_not_pass(self): self.assertTrue(differences(float('nan'),1.0))
    def test_unknown_chapter_rejected(self): self.assertRaises(ValueError,load_inputs,14)
    def test_fixtures_all_synthetic(self):
        for chapter in range(15,27): self.assertIn('Synthetic',load_inputs(chapter)['data_provenance'])
    def test_source_does_not_import_network(self):
        import ast
        for file in (Path(__file__).resolve().parents[1]/'src').rglob('*.py'):
            tree=ast.parse(file.read_text())
            for node in ast.walk(tree):
                if isinstance(node,ast.Import): self.assertFalse({a.name.split('.')[0] for a in node.names}&{'requests','urllib','socket','http'})
                if isinstance(node,ast.ImportFrom): self.assertNotIn((node.module or '').split('.')[0],{'requests','urllib','socket','http'})


if __name__ == '__main__': unittest.main()
