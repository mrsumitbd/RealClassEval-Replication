import numpy as np


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
        X = np.asarray(train, dtype=np.float64)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.ndim != 2:
            raise ValueError("train must be a 1D or 2D array")
        n, d = X.shape
        if n < 2:
            raise ValueError("at least two training samples are required")
        if factor <= 0:
            raise ValueError("factor must be > 0")
        if nmin < 1:
            raise ValueError("nmin must be >= 1")
        if truncation <= 0:
            raise ValueError("truncation must be > 0")

        if weights is None:
            w = np.full(n, 1.0 / n, dtype=np.float64)
        else:
            w = np.asarray(weights, dtype=np.float64).reshape(-1)
            if w.shape[0] != n:
                raise ValueError(
                    "weights must have the same length as the number of samples")
            if np.any(w < 0):
                raise ValueError("weights must be non-negative")
            sw = float(np.sum(w))
            if not np.isfinite(sw) or sw <= 0:
                raise ValueError("sum of weights must be positive and finite")
            w = w / sw

        mu = np.sum(X * w[:, None], axis=0)
        Xm = X - mu
        # Weighted covariance (normalized to sum(weights)=1). Add small ridge for numerical stability.
        cov = Xm.T @ (Xm * w[:, None])
        # Ensure positive definiteness via ridge
        eps = 1e-12
        trace = np.trace(cov)
        if not np.isfinite(trace) or trace <= 0:
            # Fallback to identity scaled small if degenerate
            cov = np.eye(d, dtype=np.float64) * 1e-6
        else:
            cov = cov + np.eye(d, dtype=np.float64) * (eps * trace / d)

        # Cholesky for covariance
        try:
            chol_cov = np.linalg.cholesky(cov)
        except np.linalg.LinAlgError:
            # If not PD, add more ridge
            ridge = (1e-8 if trace <= 0 else 1e-8 * trace / d)
            cov = cov + np.eye(d, dtype=np.float64) * ridge
            chol_cov = np.linalg.cholesky(cov)
        inv_cov = np.linalg.solve(
            chol_cov.T, np.linalg.solve(chol_cov, np.eye(d)))
        log_det_cov = 2.0 * np.sum(np.log(np.diag(chol_cov)))

        # Bandwidth matrix H = factor^2 * cov
        self.factor = float(factor)
        self.inv_H = inv_cov / (self.factor ** 2)
        self.log_det_H = log_det_cov + 2.0 * d * np.log(self.factor)
        self.dim = d
        self.truncation = float(truncation)
        self.nmin = int(nmin)

        self.X = X
        self.w = w
        self.n = n

        # Precompute Gaussian normalizing constant for kernel with covariance H
        self._log_norm_const = -0.5 * \
            (self.dim * np.log(2.0 * np.pi) + self.log_det_H)

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        Y = np.asarray(data, dtype=np.float64)
        if Y.ndim == 1:
            Y = Y.reshape(-1, self.dim if self.dim != 1 else 1)
        if Y.ndim != 2:
            raise ValueError("data must be a 1D or 2D array")
        if Y.shape[1] != self.dim:
            raise ValueError(
                f"data dimension mismatch: expected {self.dim}, got {Y.shape[1]}")

        m = Y.shape[0]
        dens = np.empty(m, dtype=np.float64)

        invH = self.inv_H
        log_norm_const = self._log_norm_const
        trunc2 = (self.truncation ** 2)

        X = self.X
        w = self.w

        for i in range(m):
            y = Y[i]
            delta = X - y  # (n, d)
            # Mahalanobis squared distance under H
            q = delta @ invH
            d2 = np.einsum("ij,ij->i", q, delta)

            # Select indices within truncation; ensure at least nmin using nearest distances
            idx = np.where(d2 <= trunc2)[0]
            if idx.size < self.nmin:
                # take nmin nearest
                nearest = np.argpartition(d2, self.nmin - 1)[:self.nmin]
                idx = np.unique(np.concatenate((idx, nearest), axis=0))

            sel_delta = delta[idx]
            sel_w = w[idx]

            # Compute kernel contributions
            q_sel = sel_delta @ invH
            exparg = -0.5 * np.einsum("ij,ij->i", q_sel, sel_delta)
            # Renormalize weights over selected subset to mitigate truncation bias
            wsum = np.sum(sel_w)
            if wsum <= 0 or not np.isfinite(wsum):
                dens[i] = 0.0
                continue
            contrib = np.exp(exparg) * (sel_w / wsum)
            dens[i] = np.exp(log_norm_const) * np.sum(contrib)

        return dens
