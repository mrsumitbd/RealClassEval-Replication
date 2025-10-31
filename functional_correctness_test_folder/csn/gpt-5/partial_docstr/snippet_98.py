import numpy as np


class LCModel:
    def __init__(self, degree=3, reg=1e-6):
        self.degree = int(degree)
        self.reg = float(reg)
        self._fitted = False
        self._w = None
        self._sigma2 = None
        self._L = None  # Cholesky factor of (X^T X + lambda I)
        self._A = None  # (X^T X + lambda I)
        self._Xty = None
        self.config_dim = 0

    def _as_1d(self, x):
        x = np.asarray(x)
        if x.ndim == 0:
            x = x[None]
        return x.reshape(-1)

    def _time_features(self, t):
        t = self._as_1d(t)
        # Polynomial basis 0..degree
        powers = [np.ones_like(t)]
        for k in range(1, self.degree + 1):
            powers.append(t ** k)
        return np.vstack(powers).T  # shape (n, degree+1)

    def _build_z(self, configs):
        if configs is None:
            if self.config_dim == 0:
                # will be repeated via kron with broadcasting logic
                return np.ones((1, 1))
            else:
                raise ValueError(
                    "Model expects configs of dim {} but got None".format(self.config_dim))
        c = np.asarray(configs)
        if c.ndim == 1:
            c = c[None, :]
        if self._fitted and c.shape[1] != self.config_dim:
            raise ValueError("Config dim mismatch: expected {}, got {}".format(
                self.config_dim, c.shape[1]))
        # z = [1, c...]
        ones = np.ones((c.shape[0], 1))
        return np.hstack([ones, c])

    def _design_matrix(self, times, configs):
        t = self._as_1d(times)
        Phi_t = self._time_features(t)  # (n, p)
        p = Phi_t.shape[1]
        if configs is None and self.config_dim == 0:
            # Only time features
            return Phi_t
        # Ensure configs row-wise align with times
        cfg = np.asarray(configs) if configs is not None else None
        if cfg is None:
            raise ValueError("configs must be provided")
        if cfg.ndim == 1:
            # single config for all times
            cfg = np.tile(cfg, (len(t), 1))
        if cfg.shape[0] == 1 and len(t) > 1:
            cfg = np.tile(cfg, (len(t), 1))
        if cfg.shape[0] != len(t):
            raise ValueError("configs rows ({}) must match times length ({}) or be 1".format(
                cfg.shape[0], len(t)))
        Z = self._build_z(cfg)  # (n, d+1)
        # Kronecker row-wise: for each i, kron(Z[i], Phi_t[i])
        # Efficient construction using outer then reshaping
        n, dz = Z.shape
        X = np.einsum('ij,ik->ijk', Z, Phi_t).reshape(n, dz * p)
        return X

    def fit(self, times, losses, configs=None):
        times = self._as_1d(times)
        y = self._as_1d(losses)
        if times.shape[0] != y.shape[0]:
            raise ValueError("times and losses must have the same length")
        if configs is None:
            self.config_dim = 0
        else:
            c = np.asarray(configs)
            if c.ndim == 1:
                self.config_dim = c.shape[0]
            else:
                self.config_dim = c.shape[1]
        X = self._design_matrix(times, configs)
        n_features = X.shape[1]
        A = X.T @ X
        A_reg = A + self.reg * np.eye(n_features)
        Xty = X.T @ y
        # Solve for weights
        try:
            L = np.linalg.cholesky(A_reg)
            w = np.linalg.solve(L.T, np.linalg.solve(L, Xty))
        except np.linalg.LinAlgError:
            w = np.linalg.solve(A_reg, Xty)
            # Recompute a stable Cholesky if possible by adding jitter
            jitter = 1e-10
            for _ in range(5):
                try:
                    L = np.linalg.cholesky(A_reg + jitter * np.eye(n_features))
                    break
                except np.linalg.LinAlgError:
                    jitter *= 10
            else:
                L = None
            A_reg = A_reg + (jitter if L is not None else 0.0) * \
                np.eye(n_features)
        # Residual variance
        y_hat = X @ w
        dof = max(1, X.shape[0] - n_features)
        sigma2 = float(np.sum((y - y_hat) ** 2) / dof)
        self._w = w
        self._sigma2 = sigma2 if sigma2 > 0 else 1e-12
        self._A = A_reg
        self._Xty = Xty
        self._L = L
        self._fitted = True
        return self

    def _predict_core(self, X, w, L, sigma2):
        mean = X @ w
        if L is None:
            # Fallback using solve on A
            A_inv_XT = np.linalg.solve(self._A, X.T)
            q = np.sum(X * A_inv_XT.T, axis=1)
        else:
            # var = sigma2 * (1 + x^T A^{-1} x)
            # compute v = solve(L, x^T), q = sum(v^2)
            v = np.linalg.solve(L, X.T)
            q = np.sum(v * v, axis=0)
        var = sigma2 * (1.0 + q)
        return mean, var

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
        if not self._fitted:
            raise RuntimeError("Model is not fitted yet.")
        times = self._as_1d(times)
        cfg = np.asarray(config)
        if cfg.ndim == 0:
            cfg = np.array([cfg])
        if self.config_dim == 0 and cfg.size != 0:
            raise ValueError(
                "Model was fit without configs; config should be empty.")
        if self.config_dim != 0 and cfg.size != self.config_dim:
            raise ValueError("Config dim mismatch: expected {}, got {}".format(
                self.config_dim, cfg.size))
        X = self._design_matrix(times, cfg)
        mean, var = self._predict_core(X, self._w, self._L, self._sigma2)
        return mean, var

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        if not self._fitted:
            raise RuntimeError("Model is not fitted yet.")
        times = self._as_1d(times)
        obs_times = self._as_1d(obs_times)
        obs_losses = self._as_1d(obs_losses)
        if obs_times.shape[0] != obs_losses.shape[0]:
            raise ValueError(
                "obs_times and obs_losses must have the same length")
        # Build design matrices
        if self.config_dim == 0:
            cfg = None
        else:
            if config is None:
                raise ValueError(
                    "config must be provided for extend_partial when model uses configs")
            cfg = np.asarray(config)
            if cfg.ndim == 0:
                cfg = np.array([cfg])
            if cfg.size != self.config_dim:
                raise ValueError("Config dim mismatch: expected {}, got {}".format(
                    self.config_dim, cfg.size))
        X_new = self._design_matrix(times, cfg)
        X_obs = self._design_matrix(obs_times, cfg if cfg is None else cfg)
        # Posterior update with partial observations:
        # Prec_post = A + X_obs^T X_obs
        # mean_post = Prec_post^{-1} (Xty + X_obs^T y_obs)
        A_post = self._A + (X_obs.T @ X_obs)
        b_post = self._Xty + (X_obs.T @ obs_losses)
        # Solve for posterior mean and its Cholesky
        try:
            L_post = np.linalg.cholesky(A_post)
            w_post = np.linalg.solve(L_post.T, np.linalg.solve(L_post, b_post))
        except np.linalg.LinAlgError:
            w_post = np.linalg.solve(A_post, b_post)
            L_post = None
        mean, var = self._predict_core(
            X_new, w_post, L_post if L_post is not None else None, self._sigma2)
        return mean, var
