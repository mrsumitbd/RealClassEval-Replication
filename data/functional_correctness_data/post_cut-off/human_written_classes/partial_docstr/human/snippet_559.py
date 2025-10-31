import keras
from keras import ops
import numpy as np

class SubsetOperator:
    """SubsetOperator applies the Gumbel-Softmax trick for continuous top-k selection.

    Args:
        k (int): The number of elements to select.
        tau (float, optional): The temperature parameter for Gumbel-Softmax. Defaults to 1.0.
        hard (bool, optional): Whether to use straight-through Gumbel-Softmax. Defaults to False.

    Sources:
        - `Reparameterizable Subset Sampling via Continuous Relaxations <https://github.com/ermongroup/subsets>`_
        - `Sampling Subsets with Gumbel-Top Relaxations <https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/DL2/sampling/subsets.html>`_
    """

    def __init__(self, k, tau=1.0, hard=False, n_value_dims=1):
        self.k = k
        self.tau = tau
        self.hard = hard
        self.EPSILON = np.finfo(np.float32).tiny
        self.n_value_dims = n_value_dims

    def gumbel_sample(self, shape):
        """Samples from Gumbel(0,1) distribution"""
        uniform = keras.random.uniform(shape, minval=0, maxval=1)
        return -ops.log(-ops.log(uniform + self.EPSILON) + self.EPSILON)

    def __call__(self, scores):
        gumbel_noise = self.gumbel_sample(ops.shape(scores))
        scores = scores + gumbel_noise
        khot = ops.zeros_like(scores)
        onehot_approx = ops.zeros_like(scores)
        for _ in range(self.k):
            khot_mask = ops.max(1.0 - onehot_approx, self.EPSILON)
            scores = scores + ops.log(khot_mask)
            onehot_approx = ops.softmax(scores / self.tau, axis=1)
            khot = khot + onehot_approx
        if self.hard:
            res = hard_straight_through(khot, self.k, self.n_value_dims)
        else:
            res = khot
        return res