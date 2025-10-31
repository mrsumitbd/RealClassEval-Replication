
import numpy as np


class MegKDE:
    """
    A simple multivariate kernel density estimator with optional weights,
    bandwidth scaling, truncation, and a minimum neighbor threshold.
    """

    def __init__(
        self,
        train: np.ndarray,
        weights: np.ndarray | None = None,
        truncation: float = 3.0,
        nmin: int = 4,
        factor: float = 1.0,
    ):
        """
        Parameters
        ----------
        train : np.ndarray
            Training data of shape (n_samples, n_features).
        weights : np.ndarray | None, optional
            Weights for each training sample. If None, equal weights are used.
        truncation : float, optional
            Truncation threshold in units of bandwidth (default 3.0).
        nmin : int, optional
            Minimum number of neighbors to consider when computing density.
            (Not used in this implementation but kept for API compatibility.)
        factor : float, optional
            Scaling factor for the bandwidth (default 1.0).
        """
        self.train = np.asarray(train, dtype=float)
        if self.train.ndim == 1:
            self.train = self.train[:, None]  # make it 2D

        self.n_samples, self.n_features = self.train.shape

        if weights is None:
            self.weights = np.ones(self.n_samples, dtype=float)
        else:
            self.weights = np.asarray(weights, dtype=float)
            if self.weights.shape != (self.n_samples,):
                raise ValueError("weights must have shape (n_samples,)")
        # Normalize weights to sum to 1
        wsum = self.weights.sum()
        if wsum == 0:
            raise ValueError("sum of weights must be > 0")
        self.weights = self.weights / wsum

        self.truncation = float(truncation)
        self.nmin = int(nmin)
        self.factor = float(factor)

        # Bandwidth estimation (Silverman's rule of thumb)
        # For each dimension: h_j = factor * (4 * sigma_j^5 / (3 * n))^(1/5)
        sigma = np.std(self.train, axis=0, ddof=1)
        # Avoid zero std
        sigma = np.where(sigma == 0, 1e-6, sigma)
        self.bandwidth = self.factor * \
            (4 * sigma**5 / (3 * self.n_samples)) ** (1 / 5)
        # Ensure bandwidth is positive
        self.bandwidth = np.maximum(self.bandwidth, 1e-6)

        # Precompute constants
        self.norm_const = 1.0 / \
            (self.n_samples * np.prod(self.bandwidth)
             * (2 * np.pi) ** (self.n_features / 2))

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        """
        Evaluate the KDE at the given data points.

        Parameters
        ----------
        data : np.ndarray
            Query points of shape (m_samples, n_features).

        Returns
        -------
        densities : np.ndarray
            Estimated densities at each query point, shape (m_samples,).
        """
        data = np.asarray(data, dtype=float)
        if data.ndim == 1:
            data = data[:, None]
        if data.shape[1] != self.n_features:
            raise ValueError(
                "data must have the same number of features as train")

        # Compute differences: shape (m, n, d)
        diff = (data[:, None, :] - self.train[None, :, :]) / \
            self.bandwidth[None, None, :]

        # Truncate: mask where all dimensions within truncation
        mask = np.all(np.abs(diff) <= self.truncation, axis=2)

        # Compute Gaussian kernel product
        # K(u) = exp(-0.5 * sum(u^2)) / (2π)^(d/2)
        # We already have norm_const including (2π)^(d/2)
        sq_norm = np.sum(diff**2, axis=2)
        kernel_vals = np.exp(-0.5 * sq_norm) * mask

        # Weighted sum over training points
        weighted_kernel = kernel_vals * self.weights[None, :]

        densities = self.norm_const * np.sum(weighted_kernel, axis=1)

        return densities
