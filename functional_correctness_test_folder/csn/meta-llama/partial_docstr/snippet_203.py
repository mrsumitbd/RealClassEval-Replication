
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
        self._precompute_kernel_params()

    def _compute_bandwidth(self):
        # Compute the weighted covariance matrix
        weighted_cov = np.cov(self.train, rowvar=False, aweights=self.weights)

        # Compute the bandwidth matrix
        self.bandwidth = self.factor * np.linalg.cholesky(weighted_cov)

    def _precompute_kernel_params(self):
        self.kernel_params = []
        for i in range(self.n_samples):
            mean = self.train[i]
            cov = np.dot(self.bandwidth, self.bandwidth.T)
            self.kernel_params.append((mean, cov))

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        data = np.atleast_2d(data)
        n_eval = data.shape[0]
        densities = np.zeros(n_eval)

        for i in range(n_eval):
            point = data[i]
            density = 0.0
            for j in range(self.n_samples):
                mean, cov = self.kernel_params[j]
                weight = self.weights[j]
                deviation = np.linalg.solve(self.bandwidth, point - mean)
                if np.linalg.norm(deviation) <= self.truncation:
                    density += weight * \
                        multivariate_normal.pdf(point, mean=mean, cov=cov)
            densities[i] = density

        return densities
