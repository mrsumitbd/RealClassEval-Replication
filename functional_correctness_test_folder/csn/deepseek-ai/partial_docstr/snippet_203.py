
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

        # Compute mean and covariance
        self.mean = np.average(self.train, axis=0, weights=self.weights)
        self.cov = np.cov(self.train, rowvar=False, aweights=self.weights)

        # Compute bandwidth scaling
        h = self.n_samples ** (-1.0 / (self.n_dim + 4))
        self.bandwidth = self.cov * (h * self.factor) ** 2

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        data = np.atleast_2d(data)
        n_data = data.shape[0]
        result = np.zeros(n_data)

        for i in range(n_data):
            point = data[i]
            # Compute Mahalanobis distances
            diff = self.train - point
            inv_bandwidth = np.linalg.inv(self.bandwidth)
            distances = np.sqrt(np.sum(diff @ inv_bandwidth * diff, axis=1))

            # Select points within truncation distance
            mask = distances <= self.truncation
            selected_points = self.train[mask]
            selected_weights = self.weights[mask]

            if len(selected_points) < self.nmin:
                # Fall back to global KDE if too few points
                kde = multivariate_normal(mean=self.mean, cov=self.bandwidth)
                result[i] = kde.pdf(point)
            else:
                # Local KDE using selected points
                local_mean = np.average(
                    selected_points, axis=0, weights=selected_weights)
                local_cov = np.cov(
                    selected_points, rowvar=False, aweights=selected_weights)
                kde = multivariate_normal(
                    mean=local_mean, cov=local_cov + self.bandwidth)
                result[i] = kde.pdf(point)

        return result
