
import numpy as np
from scipy.stats import norm


class MegKDE:

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None, truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        self.train = np.asarray(train)
        if self.train.ndim == 1:
            self.train = self.train[:, None]
        self.n, self.d = self.train.shape
        if weights is not None:
            self.weights = np.asarray(weights)
            if self.weights.shape[0] != self.n:
                raise ValueError(
                    "weights must have the same length as train data")
            self.weights = self.weights / np.sum(self.weights)
        else:
            self.weights = np.ones(self.n) / self.n
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor
        # Silverman's rule of thumb for bandwidth
        std = np.std(self.train, axis=0, ddof=1)
        iqr = np.subtract(*np.percentile(self.train, [75, 25], axis=0))
        sigma = np.minimum(std, iqr / 1.349)
        self.bandwidth = self.factor * \
            (0.9 * sigma * self.n ** (-1.0 / (self.d + 4)))
        self.bandwidth[self.bandwidth == 0] = 1e-6

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        data = np.asarray(data)
        if data.ndim == 1:
            data = data[:, None]
        m = data.shape[0]
        result = np.zeros(m)
        for i in range(m):
            x = data[i]
            # Compute Mahalanobis-like distance (diagonal bandwidth)
            diffs = (self.train - x) / self.bandwidth
            distsq = np.sum(diffs ** 2, axis=1)
            mask = distsq <= self.truncation ** 2
            if np.sum(mask) < self.nmin:
                # Use all points if not enough neighbors
                mask = np.ones(self.n, dtype=bool)
            # Gaussian kernel
            kernel_vals = np.exp(-0.5 * distsq[mask]) / np.prod(
                self.bandwidth) / (2 * np.pi) ** (self.d / 2)
            weighted = kernel_vals * self.weights[mask]
            result[i] = np.sum(weighted)
        return result
