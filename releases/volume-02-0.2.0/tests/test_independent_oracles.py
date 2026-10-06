"""Independent review oracles. These do not read companion expected-result files."""
import math, sys, unittest
from pathlib import Path
from fractions import Fraction
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from volume2_companion import chapter15 as a, chapter16 as b, chapter17 as c, chapter18 as d
from volume2_companion import chapter19 as e, chapter20 as f, chapter21 as g, chapter22 as h
from volume2_companion import chapter23 as i, chapter24 as j, chapter25 as k, chapter26 as l
from volume2_companion.registry import load_inputs
class IndependentChecks(unittest.TestCase):
 def test_backprop_against_independent_scalar_loss(self):
  theta=np.array([.2,-.1,.3,.4,-.2]); x=[1,2]
  def loss(t):
   z=t[3]*max(0,t[0]+2*t[1]+t[2])+t[4]
   return math.log1p(math.exp(-z))
  step=1e-5
  derivative=np.array([(loss(theta+np.eye(5)[r]*step)-loss(theta-np.eye(5)[r]*step))/(2*step) for r in range(5)])
  np.testing.assert_allclose(a.gradient(theta,x,1),derivative,rtol=1e-8)
 def test_cross_correlation_explicit_reversal(self):
  x=[2,3,5,4];kernel=[1,-1]
  np.testing.assert_array_equal(b.cross_correlation(x,kernel),np.convolve(x,kernel[::-1],'valid'))
  self.assertFalse(np.array_equal(b.cross_correlation(x,kernel),np.convolve(x,kernel,'valid')))
 def test_attention_oracle_and_causal_prefix(self):
  q=np.eye(2);v=np.array([[2,0],[0,4]])
  _,w,o=c.attention(q,q,v)
  u=math.exp(1/math.sqrt(2));expected=np.array([[1,0],[1/(1+u),u/(1+u)]])
  np.testing.assert_allclose(w,expected);np.testing.assert_allclose(o,expected@v)
  _,_,one=c.attention(q[:1],q[:1],v[:1]);np.testing.assert_array_equal(o[:1],one)
 def test_attention_unmasked_permutation_equivariance(self):
  rng=np.random.default_rng(2026);q=rng.normal(size=(4,3));v=rng.normal(size=(4,2));p=[2,0,3,1]
  expected=c.attention(q,q,v,False)[2][p]
  np.testing.assert_allclose(c.attention(q[p],q[p],v[p],False)[2],expected,atol=1e-12)
 def test_lm_cross_entropy_without_companion_helpers(self):
  nll=d.negative_log_likelihood(['a','b','c','d'],[.5,.25,.125,.125],['a','b','c'])
  self.assertAlmostEqual(nll,math.log(4))
 def test_dpo_closed_form_and_reference_reversal(self):
  r=e.dpo(.6,.2,.4,.4,.5)
  self.assertAlmostEqual(r['loss'],math.log1p(1/math.sqrt(3)))
  self.assertAlmostEqual(r['log_probability_gradients'][0],-.5/(1+math.sqrt(3)))
  self.assertAlmostEqual(e.dpo(.6,.2,.6,.2,.5)['loss'],math.log(2))
 def test_lora_non_square_dimension(self):
  w=np.arange(6).reshape(2,3);aa=np.array([[1,2,3]]);bb=np.array([[2],[-1]]);x=np.array([1,-1,2])
  out=e.lora(w,aa,bb,x,scale=.5)
  np.testing.assert_allclose(out['combined_output'],w@x+.5*np.array([2,-1])*5)
 def test_access_filter_before_vector_read(self):
  docs=[{'authorized':False,'current':True,'vector':object()}, {'authorized':True,'current':False,'vector':object()}]
  self.assertEqual(f.retrieve([1,0],docs),[])
 def test_agent_permission_and_budget_boundaries(self):
  inp=load_inputs(21)['inputs']
  self.assertEqual(g.simulate(inp)['quote_total_aud'],'36.50')
  for evidence in ['missing','stale','conflicting','cross_contact_unresolved']:
   r=g.simulate(inp,evidence=evidence);self.assertIsNone(r['quote_total_aud']);self.assertLessEqual(r['tool_call_count'],2)
  self.assertEqual(g.simulate(inp,attempted_action='purchase')['tool_call_count'],0)
 def test_as_of_future_conflict_does_not_rewrite_history(self):
  r={'id':'a','entity':'P1','event_time':'2026-10-06T09:00:00Z','available_at':'2026-10-06T09:05:00Z','price_aud':12}
  future={**r,'available_at':'2026-10-06T11:00:00Z','price_aud':99}
  self.assertEqual(h.as_of([r,future],'2026-10-06T10:00:00Z',24,'P1')['price_aud'],12)
 def test_calibration_exact_fractions(self):
  expected=sum((p-y)**2 for p,y in zip([Fraction(9,10),Fraction(8,10),Fraction(7,10),Fraction(6,10)],[1,1,0,1]))/4
  self.assertAlmostEqual(i.calibration([.9,.8,.7,.6],[1,1,0,1])['brier'],float(expected))
 def test_quantization_exact_fraction_mse(self):
  self.assertAlmostEqual(j.quantize([-1,-.5,0,.5,1])['mean_squared_error'],float(Fraction(2,5*254**2)),places=16)
 def test_distillation_gradient_with_independent_objective(self):
  teacher=np.array([.7,.2,.1]);student=np.array([.6,.25,.15]);z=np.log(student)
  def objective(logits):
   logq=logits-math.log(sum(math.exp(v) for v in logits))
   return sum(teacher*(np.log(teacher)-logq))
  eps=1e-5;grad=np.array([(objective(z+np.eye(3)[r]*eps)-objective(z-np.eye(3)[r]*eps))/(2*eps) for r in range(3)])
  np.testing.assert_allclose(grad,student-teacher,atol=1e-10)
  expected=z-.5*grad;expected=np.exp(expected)/np.exp(expected).sum()
  np.testing.assert_allclose(j.distill(teacher,student,steps=1)['student_after'],expected,atol=1e-11)
 def test_policy_nonboolean_flags_never_authorize(self):
  base={'action':'read_catalogue','trusted_user_authorized':True,'role_permitted':True,'arguments_valid':True,'sensitive_export':False}
  for key in ['trusted_user_authorized','role_permitted','arguments_valid']:
   self.assertEqual(k.policy({**base,key:'true'}),'deny')
 def test_tv_equals_maximum_subset_probability_gap(self):
  p=np.array([.6,.3,.1]);q=np.array([.4,.4,.2]);maximum=max(abs(sum((p-q)[r] for r in range(3) if mask&(1<<r))) for mask in range(8))
  self.assertAlmostEqual(l.total_variation(p,q),maximum)
 def test_invalid_lm_probabilities(self):
  for values in [[2.0],[float('nan')],[1.0,2.0]]:
   with self.assertRaises(ValueError):d.negative_log_likelihood(['a'],values,['a'])
 def test_extreme_valid_dpo_probabilities(self):
  out=e.dpo(.5,1e-320,.4,.4,.5)
  self.assertTrue(math.isfinite(out['loss']))
 def test_cosine_scaling_invariance_extreme_finite(self):
  self.assertAlmostEqual(f.cosine([1e200,1e200],[1e200,1e200]),1)
if __name__=='__main__':unittest.main(verbosity=2)
