from scipy.stats import qmc
import paddle
import numpy as np

class Point1D:

    def __init__(self, x_lb=0.0, x_ub=1.0, dataType='float32', random_seed=None):
        self.lb = x_lb
        self.ub = x_ub
        self.dtype = dataType
        np.random.seed(random_seed)
        self.lhs_x = qmc.LatinHypercube(1, seed=random_seed)

    def inner_point(self, num_sample: int=100, method='uniform'):
        """ """
        if method == 'mesh':
            X = np.linspace(self.lb, self.ub, num_sample).reshape(-1, 1)
        elif method == 'uniform':
            X = np.random.uniform(self.lb, self.ub, num_sample).reshape(-1, 1)
        elif method == 'hypercube':
            X = qmc.scale(self.lhs_x.random(num_sample), self.lb, self.ub)
        else:
            raise NotImplementedError
        return paddle.to_tensor(data=X, dtype=self.dtype)

    def boundary_point(self):
        """ """
        raise NotImplementedError

    def weight_centers(self):
        """ """
        raise NotImplementedError

    def integral_mesh(self):
        """ """
        raise NotImplementedError