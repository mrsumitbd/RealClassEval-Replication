import paddle
import numpy as np
from scipy.stats import qmc

class Point1D:

    def __init__(self, x_lb=[0.0], x_ub=[1.0], dataType='float32', random_seed=None):
        self.lb = x_lb
        self.ub = x_ub
        self.dtype = dataType
        np.random.seed(random_seed)
        self.lhs_t = qmc.LatinHypercube(1, seed=random_seed)
        self.lhs_x = qmc.LatinHypercube(1, seed=random_seed + 10086)

    def inner_point(self, nx: int, nt: int, method='hypercube', t0=[0.0], tT=[1.0]):
        """The inner points"""
        if method == 'mesh':
            X = np.linspace(self.lb, self.ub, nx)
            T = np.linspace(t0, tT, nt)
            xx, tt = np.meshgrid(X, T)
            XT = np.vstack((xx.flatten(), tt.flatten())).T
        elif method == 'uniform':
            T = np.linspace(t0, tT, nt).repeat(nx, axis=0)
            X = np.random.uniform(self.lb, self.ub, nx * nt).reshape(-1, 1)
            XT = np.vstack((X.flatten(), T.flatten())).T
        elif method == 'hypercube':
            T = np.linspace(t0, tT, nt).repeat(nx, axis=0)
            X = qmc.scale(self.lhs_x.random(nx * nt), self.lb, self.ub)
            XT = np.vstack((X.flatten(), T.flatten())).T
        else:
            raise NotImplementedError
        return paddle.to_tensor(data=XT, dtype=self.dtype)

    def boundary_point(self, num_sample: int, t0=[0.0], tT=[1.0]):
        """The boundary points"""
        T = np.linspace(t0, tT, num_sample)
        X = np.array(self.lb).repeat(num_sample, axis=0)
        XT_lb = np.vstack((X.flatten(), T.flatten())).T
        X = np.array(self.ub).repeat(num_sample, axis=0)
        XT_ub = np.vstack((X.flatten(), T.flatten())).T
        return (paddle.to_tensor(data=XT_lb, dtype=self.dtype), paddle.to_tensor(data=XT_ub, dtype=self.dtype))

    def init_point(self, num_sample: int, t_stamp=[0.0], method='mesh'):
        """The initial points"""
        if method == 'mesh':
            X = np.linspace(self.lb, self.ub, num_sample)
        elif method == 'uniform':
            X = np.random.uniform(self.lb, self.ub, num_sample).reshape(-1, 1)
        elif method == 'hypercube':
            X = qmc.scale(self.lhs_x.random(num_sample), self.lb, self.ub)
        else:
            raise NotImplementedError
        T = np.array(t_stamp).repeat(num_sample, axis=0)
        XT = np.vstack((X.flatten(), T.flatten())).T
        return paddle.to_tensor(data=XT, dtype=self.dtype)

    def weight_centers(self, n_center: int, nt: int, Rmax: float=0.0001, Rmin: float=0.0001, method='hypercube', t0=[0.0], tT=[1.0]):
        """Generate centers of compact support regions for test functions"""
        if Rmax < Rmin:
            raise ValueError('R_max should be larger than R_min.')
        elif 2.0 * Rmax > np.min(np.array(self.ub) - np.array(self.lb)):
            raise ValueError('R_max is too large.')
        elif Rmin < 0.0001 and self.dtype == 'float32':
            raise ValueError('R_min<1e-4 when data_type is paddle.float32!')
        elif Rmin < 1e-10 and self.dtype == 'float64':
            raise ValueError('R_min<1e-10 when data_type is paddle.float64!')
        R = np.random.uniform(Rmin, Rmax, [n_center * nt, 1])
        lb, ub = (np.array(self.lb) + R, np.array(self.ub) - R)
        if method == 'mesh':
            X = np.linspace([0.0], [1.0], n_center)
            T = np.linspace(t0, tT, nt)
            xx, tt = np.meshgrid(X, T)
            X, T = (xx.reshape(-1, 1), tt.reshape(-1, 1))
        elif method == 'uniform':
            X = np.random.uniform([0.0], [1.0], n_center * nt).reshape(-1, 1)
            T = np.linspace(t0, tT, nt).repeat(n_center, axis=0)
        elif method == 'hypercube':
            X = self.lhs_x.random(n_center * nt)
            T = np.linspace(t0, tT, nt).repeat(n_center, axis=0)
        else:
            raise NotImplementedError
        xc = X * (ub - lb) + lb
        return (paddle.to_tensor(data=xc, dtype=self.dtype).view(-1, 1, 1), paddle.to_tensor(data=T, dtype=self.dtype).view(-1, 1, 1), paddle.to_tensor(data=R, dtype=self.dtype).view(-1, 1, 1))

    def integral_grid(self, n_mesh_or_grid: int=9, method='mesh'):
        """Meshgrid for calculating integrals in [-1.,1.]"""
        if method == 'mesh':
            grid = np.linspace(-1.0, 1.0, n_mesh_or_grid).reshape(-1, 1)
        else:
            raise NotImplementedError(f'No {method} method.')
        return paddle.to_tensor(data=grid, dtype=self.dtype)