
import numpy as np
from scipy.spatial.distance import mahalanobis


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
        self.train = np.atleast_2d(train)
        self.n_samples, self.n_dim = self.train.shape
        self.weights = np.ones(self.n_samples) if weights is None else weights
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor

        self._compute_covariance()

    def _compute_covariance(self):
        self.covariance = np.cov(
            self.train, rowvar=False, aweights=self.weights)
        self.inv_covariance = np.linalg.inv(self.covariance)
        self.det_covariance = np.linalg.det(self.covariance)

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        '''Estimate un-normalised probability density at target points
        Args:
            data (np.ndarray): 2D array of shape (n_samples, n_dim).
        Returns:
            np.ndarray: A `(n_samples)` length array of estimates
        '''
        data = np.atleast_2d(data)
        n_data_samples, _ = data.shape
        density = np.zeros(n_data_samples)

        for i in range(n_data_samples):
            distances = np.array([mahalanobis(
                data[i], self.train[j], self.inv_covariance) for j in range(self.n_samples)])
            mask = distances <= self.truncation
            if np.sum(mask) >= self.nmin:
                weights = self.weights[mask]
                distances = distances[mask]
                kernel = np.exp(-0.5 * distances**2) / \
                    np.sqrt((2 * np.pi)**self.n_dim * self.det_covariance)
                density[i] = np.sum(weights * kernel)

        return density * self.factor
