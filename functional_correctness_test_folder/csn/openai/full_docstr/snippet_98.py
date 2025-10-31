
import numpy as np


class LCModel:
    '''
    Base class for simple learning curve models.
    Implements a very light‑weight linear regression approach.
    '''

    def __init__(self):
        # Parameters learned during fit
        self._global_times = None
        self._global_mean = None
        self._global_std = None

    def fit(self, times, losses, configs=None):
        '''
        Train the model on the observed data.
        Parameters
        ----------
        times : list of np.ndarray
            List of arrays containing the time steps for each curve.
        losses : list of np.ndarray
            List of arrays containing the loss values for each curve.
        configs : list or None
            List of configuration arrays for each sample (ignored in this base model).
        '''
        # Flatten all times and losses into a dictionary keyed by time
        time_to_losses = {}
        for t_arr, l_arr in zip(times, losses):
            for t, l in zip(t_arr, l_arr):
                time_to_losses.setdefault(t, []).append(l)

        # Sort times
        sorted_times = np.array(sorted(time_to_losses.keys()))
        means = np.array([np.mean(time_to_losses[t]) for t in sorted_times])
        stds = np.array([np.std(time_to_losses[t], ddof=1) if len(time_to_losses[t]) > 1 else 0.0
                         for t in sorted_times])

        self._global_times = sorted_times
        self._global_mean = means
        self._global_std = stds

    def predict_unseen(self, times, config):
        '''
        Predict the loss of an unseen configuration.
        Parameters
        ----------
        times : np.ndarray
            Times where to predict the loss.
        config : np.ndarray
            Numerical representation of the config (ignored in this base model).
        Returns
        -------
        mean : np.ndarray
            Mean prediction at input times.
        var : np.ndarray
            Variance prediction at input times.
        '''
        if self._global_times is None:
            raise RuntimeError("Model has not been fitted yet.")

        # Interpolate mean and std
        mean_pred = np.interp(times, self._global_times, self._global_mean)
        std_pred = np.interp(times, self._global_times, self._global_std)
        var_pred = std_pred ** 2
        return mean_pred, var_pred

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        '''
        Extend a partially observed curve.
        Parameters
        ----------
        times : np.ndarray
            Times where to predict the loss.
        obs_times : np.ndarray
            Times where the curve has already been observed.
        obs_losses : np.ndarray
            Corresponding observed losses.
        config : np.ndarray or None
            Numerical representation of the config (ignored in this base model).
        Returns
        -------
        mean : np.ndarray
            Mean prediction at input times.
        var : np.ndarray
            Variance prediction at input times.
        '''
        # Fit a simple linear regression to the observed data
        if len(obs_times) < 2:
            # Not enough data to fit; return constant predictions
            mean_pred = np.full_like(
                times, obs_losses.mean() if len(obs_losses) > 0 else 0.0)
            var_pred = np.full_like(times, 0.0)
            return mean_pred, var_pred

        # Compute slope and intercept
        X = obs_times
        y = obs_losses
        X_mean = X.mean()
        y_mean = y.mean()
        cov_xy = np.sum((X - X_mean) * (y - y_mean))
        var_x = np.sum((X - X_mean) ** 2)
        slope = cov_xy / var_x if var_x != 0 else 0.0
        intercept = y_mean - slope * X_mean

        # Predict mean
        mean_pred = slope * times + intercept

        # Estimate residual variance
        residuals = y - (slope * X + intercept)
        dof = max(len(obs_times) - 2, 1)
        residual_var = np.sum(residuals ** 2) / dof

        # For simplicity, use constant variance across times
        var_pred = np.full_like(times, residual_var)
        return mean_pred, var_pred
