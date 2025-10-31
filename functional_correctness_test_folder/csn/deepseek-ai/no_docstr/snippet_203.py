
import numpy as np
from scipy.stats import gaussian_kde


class MegKDE:

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None, truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        self.train = train
        self.weights = weights
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor
        self.kde = gaussian_kde(train.T, weights=weights)

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        return self.kde(data.T) * self.factor
