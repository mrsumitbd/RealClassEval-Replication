
import numpy as np
from scipy.stats import multivariate_normal


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

        if weights is None:
            self.weights = np.ones(self.n_samples) / self.n_samples
        else:
            self.weights = weights / np.sum(weights)

        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor

        self._compute_bandwidth()

    def _compute_bandwidth(self):
        # Compute weighted mean
        self.mean = np.average(self.train, axis=0, weights=self.weights)

        # Compute weighted covariance
        centered_train = self.train - self.mean
        self.cov = np.average(
            centered_train[:, :, np.newaxis] * centered_train[:, np.newaxis, :], axis=0, weights=self.weights)

        # Ensure covariance matrix is positive definite
        self.cov = self._ensure_positive_definite(self.cov)

        # Compute bandwidth
        self.bandwidth = self.factor * (4 / (self.n_dim + 2)) ** (1 / (self.n_dim + 4)) * \
            self.n_samples ** (-1 / (self.n_dim + 4)) * \
            np.sqrt(np.diag(self.cov)).mean()

    def _ensure_positive_definite(self, cov):
        # Ensure covariance matrix is positive definite by adding a small value to the diagonal
        eigvals = np.linalg.eigvals(cov)
        if np.any(eigvals < 0):
            cov += np.eye(self.n_dim) * (np.abs(np.min(eigvals)) + 1e-6)
        return cov

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        '''Estimate un-normalised probability density at target points
        Args:
            data (np.ndarray): 2D array of shape (n_samples, n_dim).
        Returns:
            np.ndarray: A `(n_samples)` length array of estimates
        '''
        data = np.atleast_2d(data)
        n_eval_samples, _ = data.shape

        # Compute probability density at target points
        densities = np.zeros(n_eval_samples)
        for i in range(self.n_samples):
            dist = np.linalg.solve(np.linalg.cholesky(
                self.cov), (data - self.train[i]).T).T
            mask = np.linalg.norm(dist, axis=1) < self.truncation
            densities[mask] += self.weights[i] * multivariate_normal.pdf(
                dist[mask], mean=np.zeros(self.n_dim), cov=np.eye(self.n_dim) / self.bandwidth**2)

        densities /= self.bandwidth ** self.n_dim

        return densities
