
import numpy as np
from scipy.spatial import distance_matrix


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
        self.train = train
        self.weights = np.ones(train.shape[0]) if weights is None else weights
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor
        self.bandwidth = self._estimate_bandwidth()

    def _estimate_bandwidth(self) -> float:
        # Simple heuristic for bandwidth estimation
        n_samples, n_dim = self.train.shape
        if n_samples < self.nmin:
            raise ValueError(
                f"Not enough samples to estimate density. Need at least {self.nmin} samples.")
        cov = np.cov(self.train, rowvar=False, aweights=self.weights)
        return self.factor * np.power(n_samples, -1. / (n_dim + 4)) * np.sqrt(np.linalg.det(cov))

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        n_samples, n_dim = self.train.shape
        if data.shape[1] != n_dim:
            raise ValueError(
                "Data dimension does not match training data dimension.")

        distances = distance_matrix(data, self.train)
        kernel_values = np.exp(-0.5 * (distances / self.bandwidth) ** 2)
        kernel_values[distances > self.truncation * self.bandwidth] = 0

        weighted_kernel_values = kernel_values * self.weights
        density_estimates = np.sum(
            weighted_kernel_values, axis=1) / np.sum(self.weights)

        return density_estimates
