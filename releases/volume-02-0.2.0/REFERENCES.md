# Primary and official references

These references explain the methods; they are not package dependencies. Chapter manuscripts contain their full reading lists. Web page availability was checked for the core sources noted in the execution report; no claim is made that this companion reproduces entire research papers.

- Attention: Vaswani et al. (2017), Attention Is All You Need. https://arxiv.org/abs/1706.03762
- Direct preference optimization: Rafailov et al. (2023), Direct Preference Optimization. https://arxiv.org/abs/2305.18290
- LoRA: Hu et al. (2021), LoRA: Low-Rank Adaptation of Large Language Models. https://arxiv.org/abs/2106.09685
- Distillation: Hinton et al. (2015), Distilling the Knowledge in a Neural Network. https://arxiv.org/abs/1503.02531
- NumPy reference: https://numpy.org/doc/2.3/reference/
- NumPy installation: https://numpy.org/install/
- Python unittest: https://docs.python.org/3.12/library/unittest.html

Lab distinctions: the token-count model is not a neural language model; the supplied merge sequence is not a trained tokenizer; the scaling values are constructed; the retrieval vectors are lexical and not learned semantic embeddings; the distillation lab trains only three categorical logits; the policy fixture is not an adversarially validated security system; latency values are assumed rather than measured GPU timings.

## Release 0.2.0 training mathematics bridges

- Duchi, Hazan and Singer (2011). Adaptive Subgradient Methods for Online Learning and Stochastic Optimization. https://jmlr.org/papers/v12/duchi11a.html
- Hinton, with Srivastava and Swersky. Neural Networks for Machine Learning, Lecture 6, RMSProp slides. https://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf
- Kingma and Ba (2015). Adam: A Method for Stochastic Optimization. https://arxiv.org/abs/1412.6980
- PyTorch documentation. Adagrad. https://docs.pytorch.org/docs/stable/generated/torch.optim.Adagrad.html
- PyTorch documentation. RMSprop. https://docs.pytorch.org/docs/stable/generated/torch.optim.RMSprop.html
- PyTorch documentation. Adam. https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html
- Reddi, Kale and Kumar (2018). On the Convergence of Adam and Beyond. https://arxiv.org/abs/1904.09237
- Ioffe and Szegedy (2015). Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift. https://proceedings.mlr.press/v37/ioffe15.pdf
- PyTorch documentation. BatchNorm1d. https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html
- Ba, Kiros and Hinton (2016). Layer Normalization. https://arxiv.org/abs/1607.06450
- PyTorch documentation. LayerNorm. https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html
- Santurkar et al. (2018). How Does Batch Normalization Help Optimization? https://arxiv.org/abs/1805.11604

These source URLs were opened and checked during the bridge work on 6 October 2026 UTC. Stable PyTorch links redirected to documentation labelled 2.14; only the pinned Python/NumPy runtime in environment.json was executed. The external documentation version is not a tested PyTorch dependency. RMSProp lecture slide 29 (zero-based PDF page 28) describes the moving-square idea; the exact stabilizer and variant conventions follow the explicitly stated case contract.
