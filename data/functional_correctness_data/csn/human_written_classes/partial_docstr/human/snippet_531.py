from scipy import linalg, special, stats
import numpy as np

class MeanCovTracker:
    """Tracks mean and cov of a set of points. 

    Note: points must be given as a (N,d) np.array
    """

    def __init__(self, x):
        self.N = x.shape[0]
        self.sx = x.sum(axis=0)
        self.sxxT = np.dot(x.T, x)
        self.update_mean_cov()

    def update_mean_cov(self):
        self.mean = self.sx / self.N
        self.cov = self.sxxT / self.N - xxT(self.mean)
        self.L = linalg.cholesky(self.cov, lower=True)

    def remove_point(self, x):
        self.N -= 1
        self.sx -= x
        self.sxxT -= xxT(x)
        self.update_mean_cov()

    def add_point(self, x):
        self.N += 1
        self.sx += x
        self.sxxT += xxT(x)
        self.update_mean_cov()