
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, WhiteKernel


class LCModel:
    def __init__(self):
        self.gp = None
        self.X = None
        self.y = None
        self.config_dim = None

    def fit(self, times, losses, configs=None):
        """
        Fit the model to observed learning curves.

        Parameters:
        -----------
        times: list of 1D numpy arrays
            Each array contains the time points for a single configuration.
        losses: list of 1D numpy arrays
            Each array contains the losses for a single configuration.
        configs: list of 1D numpy arrays or 2D numpy array, optional
            Each array is the numerical representation of a configuration.
        """
        X_list = []
        y_list = []
        n = len(times)
        if configs is None:
            configs = [np.zeros(1) for _ in range(n)]
        else:
            configs = [np.array(c) for c in configs]
        self.config_dim = len(configs[0])
        for t, l, c in zip(times, losses, configs):
            t = np.array(t).reshape(-1, 1)
            c = np.array(c).reshape(1, -1)
            c_tile = np.tile(c, (len(t), 1))
            X = np.hstack([t, c_tile])
            X_list.append(X)
            y_list.append(l)
        X_all = np.vstack(X_list)
        y_all = np.concatenate(y_list)
        # Kernel: time and config
        kernel = C(1.0, (1e-3, 1e3)) * \
            RBF([1.0]*(1+self.config_dim), (1e-2, 1e2)) + \
            WhiteKernel(1e-3, (1e-5, 1e1))
        self.gp = GaussianProcessRegressor(
            kernel=kernel, n_restarts_optimizer=5, normalize_y=True, random_state=0)
        self.gp.fit(X_all, y_all)
        self.X = X_all
        self.y = y_all

    def predict_unseen(self, times, config):
        '''
        predict the loss of an unseen configuration
        Parameters:
        -----------
        times: numpy array
            times where to predict the loss
        config: numpy array
            the numerical representation of the config
        Returns:
        --------
        mean and variance prediction at input times for the given config
        '''
        times = np.array(times).reshape(-1, 1)
        config = np.array(config).reshape(1, -1)
        X_pred = np.hstack([times, np.tile(config, (len(times), 1))])
        mean, std = self.gp.predict(X_pred, return_std=True)
        var = std ** 2
        return mean, var

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        """
        Fit the model to a partial learning curve (for a single config).

        Parameters:
        -----------
        times: numpy array
            times where to predict the loss
        obs_times: numpy array
            observed times
        obs_losses: numpy array
            observed losses
        config: numpy array, optional
            the numerical representation of the config
        Returns:
        --------
        mean and variance prediction at input times for the given config
        """
        if config is None:
            config = np.zeros(self.config_dim)
        obs_times = np.array(obs_times).reshape(-1, 1)
        config = np.array(config).reshape(1, -1)
        X_obs = np.hstack([obs_times, np.tile(config, (len(obs_times), 1))])
        y_obs = np.array(obs_losses)
        # Use the same kernel as in fit
        kernel = C(1.0, (1e-3, 1e3)) * \
            RBF([1.0]*(1+self.config_dim), (1e-2, 1e2)) + \
            WhiteKernel(1e-3, (1e-5, 1e1))
        gp = GaussianProcessRegressor(
            kernel=kernel, n_restarts_optimizer=3, normalize_y=True, random_state=0)
        gp.fit(X_obs, y_obs)
        times = np.array(times).reshape(-1, 1)
        X_pred = np.hstack([times, np.tile(config, (len(times), 1))])
        mean, std = gp.predict(X_pred, return_std=True)
        var = std ** 2
        return mean, var
