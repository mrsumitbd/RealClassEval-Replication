import numpy as np


class LCModel:
    '''
        base class for simple learning curve models
            '''

    def __init__(self, k_neighbors=10, min_variance=1e-8, eps=1e-12, obs_weight=5.0, exact_tol=0.0):
        self.k_neighbors = k_neighbors
        self.min_variance = min_variance
        self.eps = eps
        self.obs_weight = obs_weight
        self.exact_tol = exact_tol
        self._fitted = False
        self._train_times = None
        self._train_losses = None
        self._configs = None

    def fit(self, times, losses, configs=None):
        '''
            function to train the model on the observed data
            Parameters:
            -----------
            times: list
                list of numpy arrays of the timesteps for each curve
            losses: list
                list of numpy arrays of the loss (the actual learning curve)
            configs: list or None
                list of the configurations for each sample. Each element
                has to be a numpy array. Set to None, if no configuration
                information is available.
        '''
        if not isinstance(times, list) or not isinstance(losses, list):
            raise TypeError("times and losses must be lists of numpy arrays.")
        if len(times) != len(losses):
            raise ValueError("times and losses must have the same length.")
        if len(times) == 0:
            raise ValueError("times and losses must be non-empty.")

        flat_t = []
        flat_y = []
        for t_arr, y_arr in zip(times, losses):
            t_arr = np.asarray(t_arr).ravel()
            y_arr = np.asarray(y_arr).ravel()
            if t_arr.size != y_arr.size:
                raise ValueError(
                    "Each times array must match the size of the corresponding losses array.")
            if t_arr.size == 0:
                continue
            mask = np.isfinite(t_arr) & np.isfinite(y_arr)
            t_arr = t_arr[mask]
            y_arr = y_arr[mask]
            if t_arr.size == 0:
                continue
            flat_t.append(t_arr.astype(float))
            flat_y.append(y_arr.astype(float))

        if len(flat_t) == 0:
            raise ValueError(
                "After filtering, no valid training data points remain.")

        self._train_times = np.concatenate(flat_t, axis=0)
        self._train_losses = np.concatenate(flat_y, axis=0)

        # Sort by time for potential performance benefit (not strictly required)
        order = np.argsort(self._train_times)
        self._train_times = self._train_times[order]
        self._train_losses = self._train_losses[order]

        # Store configs as-is for API compatibility; not used in this baseline
        if configs is not None:
            if not isinstance(configs, list) or len(configs) != len(times):
                raise ValueError(
                    "configs must be a list of the same length as times and losses, or None.")
            self._configs = configs
        else:
            self._configs = None

        self._fitted = True
        return self

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
        self._check_fitted()
        q_times = self._ensure_1d_array(times, "times")
        means, vars_ = self._knn_predict(q_times,
                                         support_times=self._train_times,
                                         support_values=self._train_losses,
                                         k=self.k_neighbors,
                                         obs_weight=1.0)
        return means, vars_

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        '''
            extends a partially observed curve
            Parameters:
            -----------
            times: numpy array
                times where to predict the loss
            obs_times: numpy array
                times where the curve has already been observed
            obs_losses: numpy array
                corresponding observed losses
            config: numpy array
                numerical reperesentation of the config; None if no config
                information is available
            Returns:
            --------
            mean and variance prediction at input times

        '''
        self._check_fitted()
        q_times = self._ensure_1d_array(times, "times")
        obs_t = self._ensure_1d_array(obs_times, "obs_times")
        obs_y = self._ensure_1d_array(obs_losses, "obs_losses")
        if obs_t.size != obs_y.size:
            raise ValueError(
                "obs_times and obs_losses must have the same length.")

        if obs_t.size == 0:
            return self.predict_unseen(q_times, config)

        # Combine observed partial data with training support
        support_times = np.concatenate([obs_t, self._train_times], axis=0)
        support_values = np.concatenate([obs_y, self._train_losses], axis=0)
        means = np.empty_like(q_times, dtype=float)
        vars_ = np.empty_like(q_times, dtype=float)

        # If a query time exactly matches an observed time (within tol), return the observation
        if self.exact_tol > 0.0:
            # vectorized exact matches handling
            for i, tq in enumerate(q_times):
                diffs = np.abs(obs_t - tq)
                idx = np.argmin(diffs)
                if diffs[idx] <= self.exact_tol:
                    means[i] = obs_y[idx]
                    vars_[i] = 0.0
                else:
                    m, v = self._knn_predict_single(
                        tq,
                        support_times=support_times,
                        support_values=support_values,
                        k=self.k_neighbors,
                        obs_weight=self.obs_weight,
                        obs_count=obs_t.size
                    )
                    means[i] = m
                    vars_[i] = v
        else:
            # Also handle exact equality without tolerance
            for i, tq in enumerate(q_times):
                eq_mask = (obs_t == tq)
                if np.any(eq_mask):
                    means[i] = obs_y[np.where(eq_mask)[0][0]]
                    vars_[i] = 0.0
                else:
                    m, v = self._knn_predict_single(
                        tq,
                        support_times=support_times,
                        support_values=support_values,
                        k=self.k_neighbors,
                        obs_weight=self.obs_weight,
                        obs_count=obs_t.size
                    )
                    means[i] = m
                    vars_[i] = v

        return means, vars_

    # --------- internal helpers ---------

    def _check_fitted(self):
        if not self._fitted or self._train_times is None or self._train_losses is None:
            raise RuntimeError(
                "Model is not fitted. Call fit(...) before prediction.")

    @staticmethod
    def _ensure_1d_array(arr, name):
        arr = np.asarray(arr)
        if arr.ndim == 0:
            arr = arr.reshape(1)
        elif arr.ndim > 1:
            arr = arr.ravel()
        if arr.size == 0:
            return arr.astype(float)
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError(f"{name} must be numeric.")
        return arr.astype(float)

    def _knn_predict(self, query_times, support_times, support_values, k, obs_weight=1.0, obs_count=0):
        means = np.empty_like(query_times, dtype=float)
        vars_ = np.empty_like(query_times, dtype=float)
        for i, tq in enumerate(query_times):
            m, v = self._knn_predict_single(
                tq,
                support_times=support_times,
                support_values=support_values,
                k=k,
                obs_weight=obs_weight,
                obs_count=obs_count
            )
            means[i] = m
            vars_[i] = v
        return means, vars_

    def _knn_predict_single(self, tq, support_times, support_values, k, obs_weight=1.0, obs_count=0):
        n = support_times.size
        if n == 0:
            return np.nan, np.nan
        k_eff = int(max(1, min(k, n)))

        # Compute absolute time distances
        d = np.abs(support_times - tq)

        # Find k nearest neighbors
        if k_eff < n:
            idx = np.argpartition(d, k_eff - 1)[:k_eff]
            # sort selected by distance for stability
            idx = idx[np.argsort(d[idx])]
        else:
            idx = np.argsort(d)

        sel_times = support_times[idx]
        sel_values = support_values[idx]
        sel_d = np.abs(sel_times - tq)

        # Inverse distance weights with epsilon for stability
        w = 1.0 / (sel_d + self.eps)

        # Boost weights for observed points if obs_count > 0
        if obs_count > 0:
            obs_mask = idx < obs_count
            w = np.where(obs_mask, w * obs_weight, w)

        # Normalize weights
        w_sum = np.sum(w)
        if not np.isfinite(w_sum) or w_sum <= 0.0:
            w = np.full_like(w, 1.0 / w.size)

        mean = np.sum(w * sel_values) / np.sum(w)

        # Weighted variance
        diff = sel_values - mean
        # Use stable computation with small ridge to avoid zero variance
        var_num = np.sum(w * diff * diff)
        var_den = np.sum(w)
        var = var_num / max(self.eps, var_den)
        var = float(max(var, self.min_variance))
        return float(mean), var
