
import numpy as np


class MegKDE:
    '''Matched Elliptical Gaussian Kernel Density Estimator
    Adapted from the algorithm specified in the BAMBIS's model specified Wolf 2017
    to support weighted samples.
    '''

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None,
                 truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        '''
        Args:
            train (np.ndarray): The training data set. Should be a 1D array of samples or a 2D array
                of shape (n_samples, n_dim).
            weights (np.ndarray, optional): An array of weights. If not specified, equal weights are assumed.
            truncation (float, optional): The maximum deviation (in sigma) to use points in the KDE
            nmin (int, optional): The minimum number of points required to estimate the density
            factor (float, optional): Send bandwidth to this factor of the data estimate
        '''
        # Ensure train is 2D
        train = np.atleast_2d(train)
        if train.ndim == 1:
            train = train.reshape(-1, 1)

        self.train = train.astype(float)
        self.n_samples, self.n_dim = self.train.shape

        if weights is None:
            weights = np.ones(self.n_samples, dtype=float)
        else:
            weights = np.asarray(weights, dtype=float)
            if weights.shape[0] != self.n_samples:
                raise ValueError(
                    "weights length must match number of training samples")

        self.weights = weights
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor

        if self.n_samples < self.nmin:
            raise ValueError(f"Number of training samples ({self.n_samples}) "
                             f"is less than the required minimum ({self.nmin})")

        # Weighted mean
        w_sum = np.sum(self.weights)
        self.mean = np.average(self.train, axis=0, weights=self.weights)

        # Weighted covariance
        diff = self.train - self.mean
        # Compute weighted outer product sum
        cov = np.einsum('i,ij,ik->jk', self.weights, diff, diff) / w_sum
        # Ensure covariance is positive definite
        cov += 1e-12 * np.eye(self.n_dim)

        # Bandwidth matrix
        self.bandwidth = self.factor * cov
        self.bandwidth_inv = np.linalg.inv(self.bandwidth)
        self.bandwidth_det = np.linalg.det(self.bandwidth)

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        '''Estimate un-normalised probability density at target points
        Args:
            data (np.ndarray): 2D array of shape (n_samples, n_dim).
        Returns:
            np.ndarray: A `(n_samples)` length array of estimates
        '''
        data = np.atleast_2d(data)
        if data.ndim == 1:
            data = data.reshape(-1, 1)

        if data.shape[1] != self.n_dim:
            raise ValueError(
                "data dimensionality must match training data dimensionality")

        n_query = data.shape[0]
        estimates = np.empty(n_query, dtype=float)

        # Precompute truncation squared
        trunc_sq = self.truncation ** 2

        for idx, point in enumerate(data):
            diff = self.train - point  # shape (n_samples, n_dim)
            # Mahalanobis distance squared: diff @ H_inv @ diff.T for each sample
            d2 = np.einsum('ij,jk,ik->i', diff, self.bandwidth_inv, diff)
            mask = d2 <= trunc_sq
            if not np.any(mask):
                estimates[idx] = 0.0
                continue
            # Compute kernel values
            kernel_vals = np.exp(-0.5 * d2[mask])
            estimates[idx] = np.sum(self.weights[mask] * kernel_vals)

        return estimates
