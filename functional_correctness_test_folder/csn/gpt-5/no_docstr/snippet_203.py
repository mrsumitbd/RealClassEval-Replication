import numpy as np


class MegKDE:

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None, truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        self.train = np.asarray(train, dtype=float)
        if self.train.ndim == 1:
            self.train = self.train[:, None]
        self.n, self.d = self.train.shape

        if self.n < 1:
            raise ValueError("train must contain at least one sample")

        if weights is None:
            self.weights = np.full(self.n, 1.0 / self.n, dtype=float)
        else:
            w = np.asarray(weights, dtype=float)
            if w.shape[0] != self.n:
                raise ValueError("weights must have the same length as train")
            wsum = np.sum(w)
            if wsum <= 0 or not np.isfinite(wsum):
                raise ValueError("weights must sum to a positive finite value")
            self.weights = w / wsum

        self.truncation = float(truncation)
        if self.truncation <= 0:
            self.truncation = np.inf  # disable truncation if non-positive provided
        self.nmin = int(max(1, nmin))
        self.factor = float(factor)

        # Estimate bandwidth
        self.h = self._estimate_bandwidth()

    def _estimate_bandwidth(self) -> float:
        n, d = self.n, self.d

        # k-NN distance based bandwidth
        k = min(max(1, self.nmin), max(1, n - 1))  # ensure valid k
        if n == 1:
            knn_med = 0.0
        else:
            # Compute pairwise squared distances
            # Efficient squared distance computation
            x = self.train
            x2 = np.sum(x * x, axis=1)
            sqd = x2[:, None] + x2[None, :] - 2.0 * (x @ x.T)
            np.maximum(sqd, 0.0, out=sqd)
            # Exclude self-distances
            np.fill_diagonal(sqd, np.inf)
            # kth nearest neighbor distances for each point
            if k == 1:
                kth = np.min(sqd, axis=1)
            else:
                kth = np.partition(sqd, k - 1, axis=1)[:, k - 1]
            knn_dist = np.sqrt(kth)
            knn_med = np.median(knn_dist)

        # Base bandwidth from kNN and truncation
        if np.isfinite(self.truncation) and self.truncation > 0 and knn_med > 0:
            h_knn = knn_med / self.truncation
        else:
            h_knn = 0.0

        # Silverman's rule of thumb (isotropic)
        stds = np.std(self.train, axis=0,
                      ddof=1) if self.n > 1 else np.zeros(self.d)
        s = float(np.mean(stds))
        if s <= 0 or not np.isfinite(s):
            # fallback scale from data range
            rng = float(np.mean(np.ptp(self.train, axis=0)))
            if rng <= 0 or not np.isfinite(rng):
                rng = 1.0
            s = rng / 4.0
        silverman = s * (n ** (-1.0 / (d + 4)))

        h = self.factor * max(h_knn, silverman, 1e-12)
        return h

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        X = np.asarray(data, dtype=float)
        if X.ndim == 1:
            X = X[:, None]
        if X.shape[1] != self.d:
            raise ValueError("data dimensionality must match training data")

        h = self.h
        inv_h2 = 1.0 / (h * h)
        const = (1.0 / (np.sqrt(2.0 * np.pi) * h)) ** self.d

        # Compute squared distances between queries and train
        xt = self.train
        xq = X
        xt2 = np.sum(xt * xt, axis=1)
        xq2 = np.sum(xq * xq, axis=1)
        sqd = xq2[:, None] + xt2[None, :] - 2.0 * (xq @ xt.T)
        np.maximum(sqd, 0.0, out=sqd)

        if np.isfinite(self.truncation):
            r2 = (self.truncation * h) ** 2
            mask = sqd <= r2
        else:
            mask = None

        # Gaussian kernel evaluation with optional truncation mask
        Z = -0.5 * sqd * inv_h2
        if mask is not None:
            Z = np.where(mask, Z, -np.inf)

        K = np.exp(Z) * const
        dens = K @ self.weights
        return dens
