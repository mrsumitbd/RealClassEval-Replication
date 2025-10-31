
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
            self.weights = np.asarray(weights) / np.sum(weights)

        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor

        # Compute mean and covariance
        self.mean = np.average(self.train, axis=0, weights=self.weights)
        self.cov = np.cov(self.train.T, aweights=self.weights)

        # Compute bandwidth scaling
        h = self.n_samples ** (-1.0 / (self.n_dim + 4))
        self.bandwidth = self.factor * h

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        '''Estimate un-normalised probability density at target points
        Args:
            data (np.ndarray): 2D array of shape (n_samples, n_dim).
        Returns:
            np.ndarray: A `(n_samples)` length array of estimates
        '''
        data = np.atleast_2d(data)
        n_targets = data.shape[0]
        estimates = np.zeros(n_targets)

        for i in range(n_targets):
            point = data[i]
            # Compute Mahalanobis distances
            diff = self.train - point
            inv_cov = np.linalg.inv(self.cov)
            mahalanobis = np.sqrt(np.sum(diff @ inv_cov * diff, axis=1))

            # Select points within truncation
            mask = mahalanobis <= self.truncation
            selected_points = self.train[mask]
            selected_weights = self.weights[mask]

            if len(selected_points) < self.nmin:
                # Fallback to global KDE
                kde = multivariate_normal(
                    mean=self.mean, cov=self.cov * self.bandwidth**2)
                estimates[i] = kde.pdf(point)
            else:
                # Local KDE
                local_mean = np.average(
                    selected_points, axis=0, weights=selected_weights)
                local_cov = np.cov(selected_points.T,
                                   aweights=selected_weights)
                kde = multivariate_normal(
                    mean=local_mean, cov=local_cov * self.bandwidth**2)
                estimates[i] = kde.pdf(point)

        return estimates
