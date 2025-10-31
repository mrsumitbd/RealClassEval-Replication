from scipy.stats import qmc
import numpy as np
import paddle

class Point2D:

    def __init__(self, x_lb=[0.0, 0.0], x_ub=[1.0, 1.0], dataType='float32', random_seed=None):
        self.lb = x_lb
        self.ub = x_ub
        self.dtype = dataType
        np.random.seed(random_seed)
        self.lhs_t = qmc.LatinHypercube(1, seed=random_seed)
        self.lhs_x = qmc.LatinHypercube(2, seed=random_seed)

    def inner_point(self, nx: int, nt: int, method='hypercube', t0=[0.0], tT=[1.0]):
        """The inner points"""
        if method == 'mesh':
            x_mesh = np.linspace(self.lb[0], self.ub[0], nx)
            y_mesh = np.linspace(self.lb[1], self.ub[1], nx)
            x_mesh, y_mesh = np.meshgrid(x_mesh, y_mesh)
            X = np.vstack((x_mesh.flatten(), y_mesh.flatten())).T
            T = np.linspace(t0, tT, nt).repeat(tuple(X.shape)[0], axis=0)
            XT = np.concatenate([np.tile(X, (nt, 1)), T.reshape(-1, 1)], axis=-1)
        elif method == 'hypercube':
            T = np.linspace(t0, tT, nt).repeat(nx, axis=0)
            X = qmc.scale(self.lhs_x.random(nx * nt), self.lb, self.ub)
            XT = np.concatenate([X, T.reshape(-1, 1)], axis=-1)
        else:
            raise NotImplementedError
        return paddle.to_tensor(data=XT, dtype=self.dtype)

    def boundary_point(self, nx_each_edge: int, nt: int, t0=[0.0], tT=[1.0], method='hypercube'):
        """The boundary points"""
        T = np.linspace(t0, tT, nt).repeat(nx_each_edge * 4, axis=0)
        X_bd = []
        for _ in range(nt):
            for d in range(2):
                if method == 'mesh':
                    x_mesh = np.linspace(self.lb[0], self.ub[0], nx_each_edge)
                    y_mesh = np.linspace(self.lb[1], self.ub[1], nx_each_edge)
                    X_lb = np.vstack((x_mesh, y_mesh)).T
                    X_ub = np.vstack((x_mesh, y_mesh)).T
                elif method == 'uniform':
                    X_lb = np.random.uniform(self.lb, self.ub, (nx_each_edge, 2))
                    X_ub = np.random.uniform(self.lb, self.ub, (nx_each_edge, 2))
                elif method == 'hypercube':
                    X_lb = qmc.scale(self.lhs_x.random(nx_each_edge), np.array(self.lb), np.array(self.ub))
                    X_ub = qmc.scale(self.lhs_x.random(nx_each_edge), np.array(self.lb), np.array(self.ub))
                else:
                    raise NotImplementedError
                X_lb[:, d] = self.lb[d]
                X_bd.append(X_lb)
                X_ub[:, d] = self.ub[d]
                X_bd.append(X_ub)
        X_bd = np.concatenate(X_bd, axis=0)
        XT = np.concatenate([X_bd, T.reshape(-1, 1)], axis=-1)
        return paddle.to_tensor(data=XT, dtype=self.dtype)

    def init_point(self, nx_or_mesh: int, t_stamp=[0.0], method='mesh'):
        """The initial points"""
        if method == 'mesh':
            x_mesh = np.linspace(self.lb[0], self.ub[0], nx_or_mesh)
            y_mesh = np.linspace(self.lb[1], self.ub[1], nx_or_mesh)
            x_mesh, y_mesh = np.meshgrid(x_mesh, y_mesh)
            X = np.vstack((x_mesh.flatten(), y_mesh.flatten())).T
        elif method == 'uniform':
            x_rand = np.random.uniform(self.lb[0], self.ub[0], nx_or_mesh)
            y_rand = np.random.uniform(self.lb[1], self.ub[1], nx_or_mesh)
            X = np.vstack((x_rand.flatten(), y_rand.flatten())).T
        elif method == 'hypercube':
            X = qmc.scale(self.lhs_x.random(nx_or_mesh), self.lb, self.ub)
        else:
            raise NotImplementedError
        T = np.array(t_stamp).repeat(tuple(X.shape)[0], axis=0)
        XT = np.concatenate([X, T.reshape(-1, 1)], axis=-1)
        return paddle.to_tensor(data=XT, dtype=self.dtype)

    def weight_centers(self, n_center: int, nt: int, Rmax: float=0.0001, Rmin: float=0.0001, t0=[0.0], tT=[1.0]):
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
        T = np.linspace(t0, tT, nt).repeat(n_center, axis=0)
        X = self.lhs_x.random(n_center * nt)
        xc = X * (ub - lb) + lb
        return (paddle.to_tensor(data=xc, dtype=self.dtype).view(-1, 1, 2), paddle.to_tensor(data=T, dtype=self.dtype).view(-1, 1, 1), paddle.to_tensor(data=R, dtype=self.dtype).view(-1, 1, 1))

    def integral_grid(self, n_mesh_or_grid: int=9, method='mesh'):
        """Meshgrid for calculating integrals in [-1.,1.]^2"""
        if method == 'mesh':
            x_mesh, y_mesh = np.meshgrid(np.linspace(-1.0, 1.0, n_mesh_or_grid), np.linspace(-1.0, 1.0, n_mesh_or_grid))
            grid = np.concatenate([x_mesh.reshape(-1, 1), y_mesh.reshape(-1, 1)], axis=1)
            index = np.where(np.linalg.norm(grid, axis=1, keepdims=True) < 1.0)[0]
            grid_scaled = grid[index, :]
        else:
            raise NotImplementedError(f'No {method} method.')
        return paddle.to_tensor(data=grid_scaled, dtype=self.dtype)