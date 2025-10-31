
import numpy as np
from scipy.linalg import eigh


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
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor

        train = np.asarray(train)
        if train.ndim == 1:
            train = train[:, None]
        self.train = train
        self.n, self.d = train.shape

        if weights is None:
            self.weights = np.ones(self.n) / self.n
        else:
            self.weights = np.asarray(weights, dtype=float)
            if self.weights.shape[0] != self.n:
                raise ValueError(
                    "weights must have the same length as train samples")
            self.weights = self.weights / np.sum(self.weights)

        # Weighted mean
        self.mean = np.average(self.train, axis=0, weights=self.weights)

        # Weighted covariance
        xm = self.train - self.mean
        w = self.weights[:, None]
        cov = (w * xm).T @ xm / np.sum(self.weights)
        # Regularize if needed
        if np.linalg.matrix_rank(cov) < self.d:
            cov += np.eye(self.d) * 1e-8
        self.cov = cov

        # Bandwidth matrix: scale covariance by factor
        self.bandwidth = self.factor * self.cov

        # Precompute inverse and determinant for efficiency
        self.inv_bandwidth = np.linalg.inv(self.bandwidth)
        self.det_bandwidth = np.linalg.det(self.bandwidth)
        self.norm_const = 1.0 / \
            np.sqrt((2 * np.pi) ** self.d * self.det_bandwidth)

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        data = np.asarray(data)
        if data.ndim == 1:
            data = data[:, None]
        if data.shape[1] != self.d:
            raise ValueError(
                "data must have the same number of dimensions as train")

        results = np.zeros(data.shape[0])
        for i, x in enumerate(data):
            # Compute Mahalanobis distances to all training points
            diff = self.train - x
            md2 = np.einsum('ij,jk,ik->i', diff, self.inv_bandwidth, diff)
            # Truncate: only use points within truncation sigma
            mask = md2 <= self.truncation ** 2
            if np.sum(mask) < self.nmin:
                # If not enough points, use all points
                mask = np.ones(self.n, dtype=bool)
            # Compute kernel values
            kernel_vals = np.exp(-0.5 * md2[mask])
            # Weighted sum
            w = self.weights[mask]
            density = np.sum(w * kernel_vals)
            results[i] = self.norm_const * density
        return results
