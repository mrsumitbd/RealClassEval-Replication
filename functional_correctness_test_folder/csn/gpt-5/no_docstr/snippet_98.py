import numpy as np


class LCModel:
    def __init__(self):
        self.times_ = None
        self.mean_curve_ = None
        self.params_ = {}  # config -> (a, b)

    def _check_fitted(self):
        if self.times_ is None or self.mean_curve_ is None:
            raise RuntimeError("Model is not fitted. Call fit() first.")

    @staticmethod
    def _to_array(x):
        return np.asarray(x, dtype=float)

    @staticmethod
    def _affine_fit(x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        if x.ndim != 1 or y.ndim != 1:
            raise ValueError("x and y must be 1-D arrays.")
        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")
        n = len(x)
        if n == 0:
            return 1.0, 0.0
        if n == 1:
            xi, yi = float(x[0]), float(y[0])
            a = 0.0
            b = yi - a * xi
            return a, b
        X = np.vstack([x, np.ones(n)]).T
        # Solve min ||a*x + b - y||_2
        sol, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        a, b = float(sol[0]), float(sol[1])
        return a, b

    def fit(self, times, losses, configs=None):
        times = self._to_array(times)
        if times.ndim != 1:
            raise ValueError("times must be a 1-D array.")
        # Build loss matrix and config list
        if isinstance(losses, dict):
            cfgs = list(losses.keys())
            mat = []
            for c in cfgs:
                v = self._to_array(losses[c])
                if v.shape != times.shape:
                    raise ValueError(
                        "Each loss sequence must match times in length.")
                mat.append(v)
            L = np.vstack(mat)
            configs_list = cfgs
        else:
            L = self._to_array(losses)
            if L.ndim == 1:
                L = L[None, :]
            if L.ndim != 2:
                raise ValueError("losses must be a 2-D array if not a dict.")
            if L.shape[1] != times.shape[0]:
                raise ValueError("losses shape must be (n_configs, n_times).")
            if configs is None:
                configs_list = list(range(L.shape[0]))
            else:
                if len(configs) != L.shape[0]:
                    raise ValueError(
                        "configs length must match number of rows in losses.")
                configs_list = list(configs)

        self.times_ = times.copy()
        self.mean_curve_ = np.mean(L, axis=0)

        self.params_.clear()
        mc = self.mean_curve_
        for i, cfg in enumerate(configs_list):
            a, b = self._affine_fit(mc, L[i])
            self.params_[cfg] = (a, b)
        return self

    def predict_unseen(self, times, config):
        self._check_fitted()
        times = self._to_array(times)
        if times.ndim != 1:
            raise ValueError("times must be a 1-D array.")
        base = np.interp(times, self.times_, self.mean_curve_,
                         left=self.mean_curve_[0], right=self.mean_curve_[-1])
        if config in self.params_:
            a, b = self.params_[config]
        else:
            a, b = 1.0, 0.0
        return a * base + b

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        self._check_fitted()
        times = self._to_array(times)
        obs_times = self._to_array(obs_times)
        obs_losses = self._to_array(obs_losses)

        if obs_times.ndim != 1 or obs_losses.ndim != 1:
            raise ValueError("obs_times and obs_losses must be 1-D arrays.")
        if len(obs_times) != len(obs_losses):
            raise ValueError(
                "obs_times and obs_losses must have the same length.")
        if times.ndim != 1:
            raise ValueError("times must be a 1-D array.")

        # Base mean curve aligned to times
        base_full = np.interp(times, self.times_, self.mean_curve_, left=self.mean_curve_[
                              0], right=self.mean_curve_[-1])

        # For fitting parameters, use mean curve evaluated at observed times
        base_obs = np.interp(obs_times, self.times_, self.mean_curve_, left=self.mean_curve_[
                             0], right=self.mean_curve_[-1])

        if config is not None and config in self.params_ and len(obs_times) == 0:
            a, b = self.params_[config]
        else:
            # Fit affine transform to observed points
            a, b = self._affine_fit(base_obs, obs_losses)

        pred_full = a * base_full + b

        # Ensure we respect observed points exactly
        if len(obs_times) > 0:
            # Map observed times to nearest indices in 'times' for replacement
            # If 'times' not covering obs_times exactly, interpolate positions
            # Find indices where times match obs_times exactly
            # Replace values at exact matches; if no exact match, we can append or ignore
            # We'll replace at indices where |times - obs_time| is minimal if within tolerance
            assigned = np.zeros_like(pred_full, dtype=bool)
            for t_obs, y_obs in zip(obs_times, obs_losses):
                idx = int(np.argmin(np.abs(times - t_obs)))
                if np.isclose(times[idx], t_obs, rtol=0.0, atol=1e-12):
                    pred_full[idx] = y_obs
                    assigned[idx] = True
        return pred_full
