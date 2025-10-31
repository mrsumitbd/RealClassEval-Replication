
import numpy as np


class MegKDE:
    '''Matched Elliptical Gaussian Kernel Density Estimator
    Adapted from the algorithm specified in the BAMBIS's model specified Wolf 2017
    to support weighted samples.
    '''

    def __init__(self, train: np.ndarray, weights: np.ndarray | None = None,
                 truncation: float = 3.0, nmin: int = 4, factor: float = 1.0):
        """
        Args:
            train (np.ndarray): The training data set. Should be a 1D array of samples or a 2D array
                of shape (n_samples, n_dim).
            weights (np.ndarray, optional): An array of weights. If not specified, equal weights are assumed.
            truncation (float, optional): The maximum deviation (in sigma) to use points in the KDE
            nmin (int, optional): The minimum number of points required to estimate the density
            factor (float, optional): Send bandwidth to this factor of the data estimate
        """
        # Ensure train is 2D
        self.train = np.atleast_2d(train)
        if self.train.ndim == 1:
            self.train = self.train.reshape(-1, 1)
        self.n_samples, self.n_dim = self.train.shape

        # Weights
        if weights is None:
            self.weights = np.ones(self.n_samples, dtype=float)
        else:
            self.weights = np.asarray(weights, dtype=float)
            if self.weights.shape[0] != self.n_samples:
                raise ValueError(
                    "weights length must match number of training samples")
        # Normalize weights to sum to 1
        wsum = self.weights.sum()
        if wsum == 0:
            raise ValueError("sum of weights must be positive")
        self.weights = self.weights / wsum

        # Bandwidth matrix (elliptical Gaussian)
        # Weighted mean
        self.mean = np.average(self.train, axis=0, weights=self.weights)
        # Weighted covariance
        diff = self.train - self.mean
        # Compute weighted covariance matrix
        cov = np.dot((diff * self.weights[:, None]).T, diff)
        # Scale by factor
        self.bandwidth = factor * cov
        # Precompute inverse and determinant
        self.inv_bandwidth = np.linalg.inv(self.bandwidth)
        self.det_bandwidth = np.linalg.det(self.bandwidth)
        if self.det_bandwidth <= 0:
            raise ValueError("Bandwidth matrix must be positive definite")
        # Normalization constant for Gaussian kernel
        self.norm_const = 1.0 / \
            ((2 * np.pi) ** (self.n_dim / 2.0) * np.sqrt(self.det_bandwidth))

        # Truncation and minimum points
        self.truncation = truncation
        self.nmin = nmin

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        """
        Evaluate the KDE at the given data points.

        Args:
            data (np.ndarray): Points where the density is evaluated. Shape (n_eval,) or (n_eval, n_dim).

        Returns:
            np.ndarray: Density estimates at each point. Shape (n_eval,).
        """
        # Ensure data is 2D
        data = np.atleast_2d(data)
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        n_eval = data.shape[0]

        # Compute differences: shape (n_eval, n_samples, n_dim)
        diff = self.train[None, :, :] - \
            data[:, None, :]  # (n_eval, n_samples, n_dim)

        # Mahalanobis distances squared: (n_eval, n_samples)
        # Using einsum for efficient computation
        dist2 = np.einsum('ijk,kl,ijl->ij', diff, self.inv_bandwidth, diff)

        # Truncate distances
        mask = dist2 <= self.truncation ** 2

        # Count points within truncation for each evaluation point
        counts = mask.sum(axis=1)

        # Compute weighted kernel contributions
        # For points outside truncation, contribution is zero
        # shape (n_eval, n_samples)
        kernel_vals = np.exp(-0.5 * dist2) * self.weights
        kernel_vals *= mask  # zero out outside truncation

        # Sum over training points
        density = self.norm_const * kernel_vals.sum(axis=1)

        # If fewer than nmin points contribute, set density to zero
        if self.nmin > 0:
            density[counts < self.nmin] = 0.0

        return density
