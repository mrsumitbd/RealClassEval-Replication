
import numpy as np
from scipy.spatial.distance import cdist


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
        self.covariance = self._estimate_covariance()

    def _estimate_covariance(self):
        if self.train.ndim == 1:
            self.train = self.train[:, np.newaxis]
        mean = np.average(self.train, axis=0, weights=self.weights)
        diff = self.train - mean
        cov = np.average(diff[:, :, np.newaxis] * diff[:,
                         np.newaxis, :], axis=0, weights=self.weights)
        return self.factor * cov

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        '''Estimate un-normalised probability density at target points
        Args:
            data (np.ndarray): 2D array of shape (n_samples, n_dim).
        Returns:
            np.ndarray: A `(n_samples)` length array of estimates
        '''
        if data.ndim == 1:
            data = data[:, np.newaxis]
        n_data, n_dim = data.shape
        n_train = self.train.shape[0]
        if n_dim != self.train.shape[1]:
            raise ValueError(
                "Data dimension does not match training data dimension.")

        distances = cdist(data, self.train, metric='mahalanobis',
                          VI=np.linalg.inv(self.covariance))
        within_truncation = distances < self.truncation
        weights = self.weights * within_truncation
        sum_weights = np.sum(weights, axis=1)
        valid = sum_weights > 0

        density = np.zeros(n_data)
        density[valid] = np.sum(
            weights[valid] * np.exp(-0.5 * distances[valid]**2), axis=1) / sum_weights[valid]

        return density
