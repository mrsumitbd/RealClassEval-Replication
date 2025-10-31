
import numpy as np
from scipy.stats import gaussian_kde


class MegKDE:

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None, truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        self.train = train
        self.weights = weights
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor
        self.kde = self._fit_kde()

    def _fit_kde(self):
        if self.weights is not None:
            kde = gaussian_kde(
                self.train, weights=self.weights, bw_method=self.factor)
        else:
            kde = gaussian_kde(self.train, bw_method=self.factor)

        # Truncate the KDE
        self.min_val = np.min(self.train) - \
            self.truncation * np.std(self.train)
        self.max_val = np.max(self.train) + \
            self.truncation * np.std(self.train)

        return kde

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        # Ensure data is within the truncated range
        data = np.clip(data, self.min_val, self.max_val)
        return self.kde(data)
