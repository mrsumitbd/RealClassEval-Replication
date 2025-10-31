from scipy.linalg import LinAlgError, cholesky
import numpy as np

class VanishCovTracker:
    """Tracks the vanishing mean and covariance of a sequence of points.

    Computes running mean and covariance of points
    t^(-alpha) * X_t
    for some alpha \\in [0,1] (typically)
    """

    def __init__(self, alpha=0.6, dim=1, mu0=None, Sigma0=None):
        self.alpha = alpha
        self.t = 0
        self.mu = np.zeros(dim) if mu0 is None else mu0
        if Sigma0 is None:
            self.Sigma = np.eye(dim)
            self.L0 = np.eye(dim)
        else:
            self.Sigma = Sigma0
            self.L0 = cholesky(Sigma0, lower=True)
        self.L = self.L0.copy()

    def gamma(self):
        return (self.t + 1) ** (-self.alpha)

    def update(self, v):
        """Adds point v"""
        self.t += 1
        g = self.gamma()
        self.mu = (1.0 - g) * self.mu + g * v
        mv = v - self.mu
        self.Sigma = (1.0 - g) * self.Sigma + g * np.dot(mv[:, np.newaxis], mv[np.newaxis, :])
        try:
            self.L = cholesky(self.Sigma, lower=True)
        except LinAlgError:
            self.L = self.L0