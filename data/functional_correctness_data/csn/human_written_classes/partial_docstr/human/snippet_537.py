import numpy as np
from scipy.signal import choose_conv_method, correlate

class AutoCovarianceCalculator:
    """An artificial device to efficiently calculate the autocovariances based
    on (possibly) multiple runs of an MCMC method.
    """

    def __init__(self, X: np.ndarray, method: str=None, bias=True):
        """
        :param X: np array of size `(M,P)`, typically the result of `M` independent MCMC runs of length `P`
        :param method: how will the covariances be calculated. `None` to let things be chosen automatically, otherwise `direct` or `fft` must be specified.
        """
        self.X = X
        self.P, self.M = X.shape
        self.mu: float = np.mean(X)
        self.method = method
        self.bias = bias
        self._covariances = np.array([np.nan] * self.P)

    def __getitem__(self, k: int):
        if k >= len(self._covariances) or k < 0:
            raise IndexError
        if np.isnan(self._covariances[k]):
            if self.method is None:
                self._choose_method()
            if self.method == 'fft':
                self._covariances = autocovariance_fft_multiple(X=self.X, mu=self.mu, bias=self.bias)
                assert len(self._covariances) == self.P
            elif self.method == 'direct':
                self._covariances[k] = autocovariance(X=self.X, order=k, mu=self.mu, bias=self.bias)
            else:
                raise AssertionError("Method must be either 'fft' or 'direct'")
        return self._covariances[k]

    def _choose_method(self):
        if self.P <= 10:
            self.method = 'direct'
            return
        test = self.X[0:self.P // 2, 0]
        self.method = choose_conv_method(test, test)

    def __len__(self):
        return len(self._covariances)