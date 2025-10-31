
import numpy as np
from scipy.stats import gaussian_kde


class MegKDE:

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None, truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        if weights is None:
            weights = np.ones_like(train)
        self.kde = gaussian_kde(train, weights=weights)
        self.kde.covariance_factor = lambda: self.kde.scotts_factor() * factor
        self.kde._compute_covariance()
        self.truncation = truncation
        self.nmin = nmin

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        densities = self.kde.evaluate(data)
        densities[densities < np.finfo(densities.dtype).tiny] = np.finfo(
            densities.dtype).tiny
        log_densities = np.log(densities)
        log_densities = np.clip(
            log_densities, -self.truncation, self.truncation)
        return log_densities
