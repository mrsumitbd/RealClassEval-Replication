
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
        self.train = train
        self.weights = weights if weights is not None else np.ones(len(train))
        self.truncation = truncation
        self.nmin = nmin
        self.factor = factor

        if self.train.ndim == 1:
            self.train = self.train.reshape(-1, 1)

        self.n_samples, self.n_dim = self.train.shape
        self.mean = np.average(self.train, axis=0, weights=self.weights)
        self.cov = np.cov(self.train, rowvar=False, aweights=self.weights)
        self.inv_cov = np.linalg.inv(self.cov)
        self.det_cov = np.linalg.det(self.cov)

    def evaluate(self, data: np.ndarray) -> np.ndarray:
        if data.ndim == 1:
            data = data.reshape(-1, 1)

        n_data, _ = data.shape
        density = np.zeros(n_data)

        for i in range(n_data):
            distances = np.array([mahalanobis(
                data[i], self.train[j], self.inv_cov) for j in range(self.n_samples)])
            mask = distances <= self.truncation
            if np.sum(mask) >= self.nmin:
                weights = self.weights[mask]
                weights /= np.sum(weights)
                density[i] = np.sum(weights * np.exp(-0.5 * distances[mask]**2)) / \
                    (np.sqrt(self.det_cov) * (2 * np.pi)**(self.n_dim / 2))

        return density
