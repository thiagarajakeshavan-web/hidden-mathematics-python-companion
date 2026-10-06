"""Independent optimizer/normalization oracles; no expected files read."""
from decimal import Decimal, localcontext
from pathlib import Path
import math,sys,unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from volume2_companion import chapter15_optimizers as opt, chapter16_normalization as norm

def oracle(method,gradients,eta='.1',eps='.00000001',b1='.9',b2='.9'):
 with localcontext() as ctx:
  ctx.prec=60
  eta,eps,b1,b2=map(Decimal,[eta,eps,b1,b2]);s=m=v=theta=Decimal(0);answer=[]
  for t,raw in enumerate(gradients,1):
   g=Decimal(str(raw))
   if method=='adagrad':s+=g*g;num=g;den=s.sqrt()+eps
   elif method=='rmsprop':v=b2*v+(1-b2)*g*g;num=g;den=v.sqrt()+eps
   else:
    m=b1*m+(1-b1)*g;v=b2*v+(1-b2)*g*g
    num=m/(1-b1**t);den=(v/(1-b2**t)).sqrt()+eps
   theta-=eta*num/den;answer.append(float(theta))
 return answer
class BridgeReview(unittest.TestCase):
 def test_adagrad_high_precision_two_steps(self):
  np.testing.assert_allclose([r['parameter'] for r in opt.trace([2,-1],'adagrad')['steps']],oracle('adagrad',[2,-1]),rtol=1e-14)
 def test_rmsprop_high_precision_two_steps(self):
  np.testing.assert_allclose([r['parameter'] for r in opt.trace([2,-1],'rmsprop')['steps']],oracle('rmsprop',[2,-1]),rtol=1e-14)
 def test_adam_high_precision_two_steps(self):
  np.testing.assert_allclose([r['parameter'] for r in opt.trace([2,-1],'adam')['steps']],oracle('adam',[2,-1]),rtol=1e-14)
 def test_high_precision_mixed_gradient_sweep(self):
  gs=[0,3,-2,.001,-5,0,4]
  for name in ['adagrad','rmsprop','adam']:
   actual=opt.trace(gs,name,learning_rate=.03,epsilon=.25,beta1=.8,beta2=.7)
   np.testing.assert_allclose([r['parameter'] for r in actual['steps']],oracle(name,gs,'.03','.25','.8','.7'),atol=1e-14)
 def test_bias_correction_constant_gradients(self):
  r=opt.trace([3]*7,'adam',beta1=.8,beta2=.7)
  for row in r['steps']:
   self.assertAlmostEqual(row['corrected_first_moment'],3)
   self.assertAlmostEqual(row['corrected_second_moment'],9)
 def test_adam_momentum_survives_negative_current_gradient(self):
  r=opt.trace([2,-1],'adam')['steps'][1]
  self.assertLess(r['gradient'],0);self.assertGreater(r['first_moment'],0);self.assertLess(r['parameter_change'],0)
 def test_outside_root_epsilon(self):
  r=opt.trace([2],'adagrad',epsilon=.25)['steps'][0]
  self.assertAlmostEqual(r['parameter'],-.2/2.25);self.assertNotAlmostEqual(r['parameter'],-.2/math.sqrt(4.25))
 def test_optimizer_invalid_controls(self):
  for key,value in [('epsilon',0),('epsilon',float('nan')),('beta1',1),('beta2',-1),('learning_rate',False)]:
   with self.assertRaises(ValueError):opt.trace([2],'adam',**{key:value})
 def test_bn_forward_and_running_distinct_variance(self):
  r=norm.batch_norm_train([[1],[3]],[2],[.5],1e-5,[0],[1],.1)
  np.testing.assert_allclose(r['batch_mean'],[2]);np.testing.assert_allclose(r['batch_variance_biased'],[1]);np.testing.assert_allclose(r['batch_variance_unbiased'],[2])
  np.testing.assert_allclose(r['output'],[[.5-2/math.sqrt(1.00001)],[.5+2/math.sqrt(1.00001)]],atol=1e-14)
  np.testing.assert_allclose(r['updated_running_mean'],[.2]);np.testing.assert_allclose(r['updated_running_variance'],[1.1])
 def test_bn_frozen_inference_not_updated_train_state(self):
  mu=np.array([1.]);var=np.array([4.]);r=norm.batch_norm_infer([[1],[3]],[2],[.5],1e-5,mu,var)
  np.testing.assert_allclose(r['output'],[[.5],[.5+4/math.sqrt(4.00001)]],atol=1e-14)
  np.testing.assert_array_equal(mu,[1]);np.testing.assert_array_equal(var,[4])
 def test_inference_batch_composition_independent(self):
  args=([1],[0],1e-5,[1],[4])
  a=norm.batch_norm_infer([[2],[3]],*args)['output'][0]
  b=norm.batch_norm_infer([[2],[-100]],*args)['output'][0]
  np.testing.assert_array_equal(a,b)
 def test_training_batch_composition_dependent(self):
  args=([1],[0],1e-5,[0],[1],.1)
  a=norm.batch_norm_train([[2],[3]],*args)['output'][0]
  b=norm.batch_norm_train([[2],[-100]],*args)['output'][0]
  self.assertFalse(np.allclose(a,b))
 def test_bn_epsilon_prevents_exact_unit_variance(self):
  r=norm.batch_norm_train([[1],[3]],[1],[0],.5,[0],[1],.1)
  self.assertAlmostEqual(float(np.mean(r['normalized']**2)),1/1.5)
 def test_bn_vs_ln_axis_oracle(self):
  x=[[1,3],[5,7]];bn=norm.batch_norm_train(x,[1,1],[0,0],1e-5,[0,0],[1,1],.1);ln=norm.layer_norm(x,[1,1],[0,0],1e-5)
  np.testing.assert_allclose(bn['normalized'],np.array([[-2,-2],[2,2]])/math.sqrt(4.00001))
  np.testing.assert_allclose(ln['normalized'],np.array([[-1,1],[-1,1]])/math.sqrt(1.00001))
 def test_normalization_constant_input_affine_shift(self):
  r=norm.batch_norm_train([[4],[4]],[-2],[3],1e-5,[0],[1],.1)
  np.testing.assert_array_equal(r['output'],[[3],[3]])
 def test_normalization_invalid_state(self):
  with self.assertRaises(ValueError):norm.batch_norm_train([[1]],[1],[0],1e-5,[0],[1],.1)
  with self.assertRaises(ValueError):norm.batch_norm_infer([[1]],[1],[0],1e-5,[0],[-1])
if __name__=='__main__':unittest.main(verbosity=2)
