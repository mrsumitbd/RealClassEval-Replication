
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel as C


class LCModel:
    """
    A simple learning‑curve model that uses a Gaussian Process to predict
    loss values over time for a given configuration.
    """

    def __init__(self):
        self.model = None
        self.X_train = None
        self.y_train = None

    def _build_features(self, times, configs=None):
        """
        Build the feature matrix for the GP.
        Each row corresponds to a (time, config) pair.
        """
        times = np.asarray(times).reshape(-1, 1)  # shape (n_samples, 1)
        if configs is None:
            X = times
        else:
            configs = np.asarray(configs)
            if configs.ndim == 1:
                configs = configs.reshape(-1, 1)
            X = np.hstack([times, configs])  # shape (n_samples, 1 + n_config)
        return X

    def fit(self, times, losses, configs=None):
        """
        Fit the Gaussian Process model to the provided data.
        Parameters
        ----------
        times : array-like, shape (n_samples,)
            Time points at which losses were observed.
        losses : array-like, shape (n_samples,)
            Observed loss values.
        configs : array-like, shape (n_samples, n_features) or None
            Numerical representation of the configuration for each sample.
        """
        times = np.asarray(times).ravel()
        losses = np.asarray(losses).ravel()
        if times.shape != losses.shape:
            raise ValueError("times and losses must have the same shape")

        X = self._build_features(times, configs)
        y = losses

        # Kernel: Constant * Matern + White noise
        kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=1.0,
                                              nu=1.5) + WhiteKernel(noise_level=1e-5)
        self.model = GaussianProcessRegressor(
            kernel=kernel, normalize_y=True, n_restarts_optimizer=5)
        self.model.fit(X, y)

        self.X_train = X
        self.y_train = y

    def predict_unseen(self, times, config):
        """
        Predict the loss of an unseen configuration.
        Parameters
        ----------
        times : array-like, shape (n_times,)
            Times at which to predict the loss.
        config : array-like, shape (n_features,) or None
            Numerical representation of the configuration.
        Returns
        -------
        mean : ndarray, shape (n_times,)
            Predictive mean.
        var : ndarray, shape (n_times,)
            Predictive variance.
        """
        if self.model is None:
            raise RuntimeError("Model has not been fitted yet.")

        times = np.asarray(times).ravel()
        X_test = self._build_features(times, config)
        mean, std = self.model.predict(X_test, return_std=True)
        var = std ** 2
        return mean, var

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        """
        Extend the model with new partial observations.
        Parameters
        ----------
        times : array-like, shape (n_samples,)
            Time points for the new observations.
        obs_times : array-like, shape (n_samples,)
            Observed times (should match `times`).
        obs_losses : array-like, shape (n_samples,)
            Observed loss values.
        config : array-like, shape (n_features,) or None
            Numerical representation of the configuration for the new observations.
        """
        if self.model is None:
            # If no prior data, just fit with the new data
            self.fit(times, obs_losses, config)
            return

        # Combine old and new data
        new_X = self._build_features(obs_times, config)
        new_y = np.asarray(obs_losses).ravel()

        combined_X = np.vstack([self.X_train, new_X])
        combined_y = np.concatenate([self.y_train, new_y])

        # Refit the model
        self.fit(combined_X[:, 0], combined_y, combined_X[:,
                 1:] if combined_X.shape[1] > 1 else None)
