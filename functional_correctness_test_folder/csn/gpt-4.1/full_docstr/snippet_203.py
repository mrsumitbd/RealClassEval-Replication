
import numpy as np


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
        train = np.asarray(train)
        if train.ndim == 1:
            train = train[:, None]
        self.train = train
        self.n_samples, self.n_dim = train.shape

        if weights is None:
            self.weights = np.ones(self.n_samples) / self.n_samples
        else:
            self.weights = np.asarray(weights, dtype=float)
            self.weights = self.weights / np.sum(self.weights)

        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor

        # Precompute global covariance and bandwidth
        mean = np.average(self.train, axis=0, weights=self.weights)
        diff = self.train - mean
        cov = np.cov(diff.T, aweights=self.weights, bias=True)
        if self.n_dim == 1:
            cov = np.atleast_2d(cov)
        self.global_cov = cov

        # Silverman's rule of thumb for bandwidth
        # h = (4/(d+2))**(1/(d+4)) * n**(-1/(d+4))
        n_eff = 1.0 / np.sum(self.weights ** 2)
        h = (4/(self.n_dim+2))**(1/(self.n_dim+4)) * n_eff**(-1/(self.n_dim+4))
        self.bandwidth = self.factor * h

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        '''Estimate un-normalised probability density at target points
        Args:
            data (np.ndarray): 2D array of shape (n_samples, n_dim).
        Returns:
            np.ndarray: A `(n_samples)` length array of estimates
        '''
        data = np.asarray(data)
        if data.ndim == 1:
            data = data[:, None]
        n_eval = data.shape[0]
        result = np.zeros(n_eval)

        for i in range(n_eval):
            x = data[i]
            # Compute Mahalanobis distances to all training points
            diffs = self.train - x
            try:
                inv_cov = np.linalg.inv(self.global_cov)
            except np.linalg.LinAlgError:
                inv_cov = np.linalg.pinv(self.global_cov)
            dists = np.einsum('ij,jk,ik->i', diffs, inv_cov, diffs)
            dists = np.sqrt(dists)
            # Select points within truncation bandwidth
            mask = dists <= self.truncation * self.bandwidth
            idx = np.where(mask)[0]
            if len(idx) < self.nmin:
                # Use nmin closest points
                idx = np.argsort(dists)[:self.nmin]
            sel_train = self.train[idx]
            sel_weights = self.weights[idx]
            # Local mean and covariance
            local_mean = np.average(sel_train, axis=0, weights=sel_weights)
            local_diff = sel_train - local_mean
            local_cov = np.cov(local_diff.T, aweights=sel_weights, bias=True)
            if self.n_dim == 1:
                local_cov = np.atleast_2d(local_cov)
            # Bandwidth scaling
            cov = local_cov * (self.bandwidth ** 2)
            try:
                inv_cov = np.linalg.inv(cov)
                det_cov = np.linalg.det(cov)
            except np.linalg.LinAlgError:
                inv_cov = np.linalg.pinv(cov)
                det_cov = np.linalg.det(cov + 1e-8 * np.eye(self.n_dim))
            # Evaluate kernel sum
            diffs = sel_train - x
            exponents = -0.5 * np.einsum('ij,jk,ik->i', diffs, inv_cov, diffs)
            norm_const = (2 * np.pi) ** (-self.n_dim / 2) * det_cov ** (-0.5)
            kernel_vals = norm_const * np.exp(exponents)
            result[i] = np.sum(sel_weights * kernel_vals)
        return result
