class MegKDE:
    '''Matched Elliptical Gaussian Kernel Density Estimator
    Adapted from the algorithm specified in the BAMBIS's model specified Wolf 2017
    to support weighted samples.
    '''

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None, truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        '''
        Args:
            train (np.ndarray): The training data set. Should be a 1D array of samples or a 2D array
                of shape (n_samples, n_dim).
            weights (np.ndarray, optional): An array of weights. If not specified, equal weights are assumed.
            truncation (float, optional): The maximum deviation (in sigma) to use points in the KDE
            nmin (int, optional): The minimum number of points required to estimate the density
            factor (float, optional): Send bandwidth to this factor of the data estimate
        '''
        if train is None:
            raise ValueError("train must be provided")
        X = np.asarray(train)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        elif X.ndim != 2:
            raise ValueError("train must be 1D or 2D array")
        n, d = X.shape

        if weights is None:
            w = np.ones(n, dtype=float)
        else:
            w = np.asarray(weights, dtype=float).reshape(-1)
            if w.shape[0] != n:
                raise ValueError(
                    "weights must have same length as number of samples")
        if np.any(w < 0):
            raise ValueError("weights must be non-negative")
        wsum = float(np.sum(w))
        if not np.isfinite(wsum) or wsum <= 0:
            raise ValueError("sum of weights must be positive and finite")

        mu = (w[:, None] * X).sum(axis=0) / wsum
        Xm = X - mu
        # Weighted covariance (second moment)
        # Use sum(w * outer) / sum(w)
        cov = (Xm.T * w) @ Xm / wsum
        # Ensure symmetry
        cov = 0.5 * (cov + cov.T)
        # Jitter for numerical stability
        eps = 1e-12
        jitter = eps * \
            np.trace(cov) / d if np.isfinite(np.trace(cov)
                                             ) and np.trace(cov) > 0 else eps
        cov = cov + np.eye(d) * jitter
        # Bandwidth matrix
        H = (factor ** 2) * cov
        # Inverse via Cholesky
        try:
            L = np.linalg.cholesky(H)
        except np.linalg.LinAlgError:
            # Add more jitter if needed
            diag_boost = max(jitter, 1e-9)
            H = H + np.eye(d) * diag_boost
            L = np.linalg.cholesky(H)
        Linv = np.linalg.inv(L)
        invH = Linv.T @ Linv

        self.train = X
        self.weights = w
        self._wsum = wsum
        self._invH = invH
        self._trunc2 = float(truncation) ** 2
        self._nmin = int(max(1, nmin))
        self._d = d
        self._n = n

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        '''Estimate un-normalised probability density at target points
        Args:
            data (np.ndarray): 2D array of shape (n_samples, n_dim).
        Returns:
            np.ndarray: A `(n_samples)` length array of estimates
        '''
        Xq = np.asarray(data)
        if Xq.ndim == 1:
            Xq = Xq.reshape(-1, self._d)
        if Xq.ndim != 2 or Xq.shape[1] != self._d:
            raise ValueError(f"data must be of shape (n_samples, {self._d})")
        m = Xq.shape[0]
        invH = self._invH
        T = self.train
        w = self.weights
        trunc2 = self._trunc2
        nmin = self._nmin

        # Compute squared Mahalanobis distances for all pairs
        # d2[i, j] = (Xq[i]-T[j])^T invH (Xq[i]-T[j])
        # Use broadcasting; may be memory heavy for very large inputs.
        diff = Xq[:, None, :] - T[None, :, :]
        tmp = diff @ invH
        d2 = np.sum(tmp * diff, axis=2)

        # Exponentials
        out = np.zeros(m, dtype=float)
        exp_full = np.exp(-0.5 * d2)

        # Apply truncation; ensure at least nmin contributors
        for i in range(m):
            mask = d2[i] <= trunc2
            if np.count_nonzero(mask) < nmin:
                # take nmin smallest distances
                idx = np.argpartition(d2[i], nmin - 1)[:nmin]
                val = np.dot(w[idx], exp_full[i, idx])
            else:
                idx = np.nonzero(mask)[0]
                val = np.dot(w[idx], exp_full[i, idx])
            out[i] = val

        return out
