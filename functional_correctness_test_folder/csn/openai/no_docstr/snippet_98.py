
import numpy as np


class LCModel:
    """
    A simple linear learning‑curve model.
    Stores a linear regression (slope & intercept) for each configuration.
    """

    def __init__(self):
        # mapping from config key to (slope, intercept)
        self._models = {}

    def _to_key(self, config):
        """Convert a config to a hashable key."""
        if config is None:
            return None
        # Assume config is a dict or any hashable object
        if isinstance(config, dict):
            # Sort items to ensure consistent ordering
            return tuple(sorted(config.items()))
        return config

    def _fit_linear(self, times, losses):
        """Fit a simple linear regression: loss = slope * time + intercept."""
        times = np.asarray(times, dtype=float)
        losses = np.asarray(losses, dtype=float)
        if times.ndim != 1 or losses.ndim != 1:
            raise ValueError("times and losses must be 1‑D arrays")
        if times.size != losses.size:
            raise ValueError("times and losses must have the same length")
        if times.size < 2:
            # Not enough points to fit a line; use constant model
            slope = 0.0
            intercept = losses.mean()
        else:
            mean_t = times.mean()
            mean_l = losses.mean()
            cov = ((times - mean_t) * (losses - mean_l)).sum()
            var = ((times - mean_t) ** 2).sum()
            slope = cov / var if var != 0 else 0.0
            intercept = mean_l - slope * mean_t
        return slope, intercept

    def fit(self, times, losses, configs=None):
        """
        Fit the model(s) to the provided data.

        Parameters
        ----------
        times : array‑like
            Training times (or epochs) for each observation.
        losses : array‑like
            Corresponding loss values.
        configs : array‑like or None
            Optional configuration identifiers for each observation.
            If None, a single global model is fitted.
        """
        times = np.asarray(times, dtype=float)
        losses = np.asarray(losses, dtype=float)

        if configs is None:
            # Single global model
            slope, intercept = self._fit_linear(times, losses)
            self._models[None] = (slope, intercept)
        else:
            configs = np.asarray(configs)
            if configs.size != times.size:
                raise ValueError("configs must have the same length as times")
            # Group by config
            unique_configs = np.unique(configs)
            for cfg in unique_configs:
                mask = configs == cfg
                slope, intercept = self._fit_linear(times[mask], losses[mask])
                self._models[self._to_key(cfg)] = (slope, intercept)

    def predict_unseen(self, times, config=None):
        """
        Predict loss values for unseen times given a configuration.

        Parameters
        ----------
        times : array‑like
            Times at which to predict loss.
        config : hashable or None
            Configuration identifier. If None, uses the global model.

        Returns
        -------
        preds : np.ndarray
            Predicted loss values.
        """
        key = self._to_key(config)
        if key not in self._models:
            raise KeyError(f"No model found for configuration {config!r}")
        slope, intercept = self._models[key]
        times = np.asarray(times, dtype=float)
        return slope * times + intercept

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        """
        Extend a partial training curve to the full set of times.

        Parameters
        ----------
        times : array‑like
            Full set of times (e.g., all epochs).
        obs_times : array‑like
            Observed times (subset of `times`).
        obs_losses : array‑like
            Observed loss values at `obs_times`.
        config : hashable or None
            Configuration identifier.

        Returns
        -------
        full_losses : np.ndarray
            Predicted loss values for all `times`.
        """
        # Fit a model to the partial data
        slope, intercept = self._fit_linear(obs_times, obs_losses)
        # Store or update the model for this config
        self._models[self._to_key(config)] = (slope, intercept)
        # Predict for all times
        times = np.asarray(times, dtype=float)
        return slope * times + intercept
