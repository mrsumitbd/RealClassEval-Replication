
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import cho_factor, cho_solve


class LCModel:

    def __init__(self):
        self.theta = None
        self.sigma_f = None
        self.sigma_n = None
        self.X = None
        self.y = None
        self.L = None
        self.alpha = None

    def _kernel(self, x1, x2):
        sqdist = np.sum(x1**2, axis=1).reshape(-1, 1) + \
            np.sum(x2**2, axis=1) - 2 * np.dot(x1, x2.T)
        return self.sigma_f**2 * np.exp(-0.5 * sqdist / self.theta**2)

    def _neg_log_likelihood(self, params):
        self.theta, self.sigma_f, self.sigma_n = params
        K = self._kernel(self.X, self.X) + \
            self.sigma_n**2 * np.eye(len(self.X))
        L, lower = cho_factor(K, lower=True)
        alpha = cho_solve((L, lower), self.y)
        log_likelihood = -0.5 * \
            np.dot(self.y.T, alpha) - np.sum(np.log(np.diag(L))) - \
            len(self.X)/2 * np.log(2*np.pi)
        return -log_likelihood

    def fit(self, times, losses, configs=None):
        if configs is None:
            configs = np.zeros((len(times), 1))
        self.X = np.column_stack((times.reshape(-1, 1), configs))
        self.y = losses.reshape(-1, 1)

        # Initial guess for theta, sigma_f, sigma_n
        initial_params = [1.0, 1.0, 0.1]
        bounds = [(1e-5, None), (1e-5, None), (1e-5, None)]
        result = minimize(self._neg_log_likelihood,
                          initial_params, bounds=bounds)
        self.theta, self.sigma_f, self.sigma_n = result.x

        K = self._kernel(self.X, self.X) + \
            self.sigma_n**2 * np.eye(len(self.X))
        self.L, lower = cho_factor(K, lower=True)
        self.alpha = cho_solve((self.L, lower), self.y)

    def predict_unseen(self, times, config):
        X_test = np.column_stack(
            (times.reshape(-1, 1), np.tile(config, (len(times), 1))))
        K_s = self._kernel(self.X, X_test)
        K_ss = self._kernel(X_test, X_test) + 1e-8 * np.eye(len(X_test))

        v = cho_solve((self.L, True), K_s)
        mu = np.dot(K_s.T, self.alpha).flatten()
        var = np.diag(K_ss - np.dot(K_s.T, v))

        return mu, var

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        if config is None:
            config = np.zeros(1)
        X_new = np.column_stack(
            (obs_times.reshape(-1, 1), np.tile(config, (len(obs_times), 1))))
        y_new = obs_losses.reshape(-1, 1)

        X_combined = np.vstack((self.X, X_new))
        y_combined = np.vstack((self.y, y_new))

        self.X = X_combined
        self.y = y_combined

        K = self._kernel(self.X, self.X) + \
            self.sigma_n**2 * np.eye(len(self.X))
        self.L, lower = cho_factor(K, lower=True)
        self.alpha = cho_solve((self.L, lower), self.y)

        return self.predict_unseen(times, config)
