import numpy as np

class KernelDensityDerivative:
    """
    Kernel density derivative estimator.

    Parameters:
        data (numpy.ndarray): Data points for density estimation.
        deriv_order (int): Order of the derivative (0 for density, 2 for second derivative).

    Attributes:
        kernel (function): Kernel function used for density estimation.
        deriv_order (int): Order of the derivative being estimated.
        h (float): Bandwidth used for the kernel density estimation.
        datah (numpy.ndarray): Scaled data by the bandwidth.
    """

    def __init__(self, data, deriv_order):
        if deriv_order == 0:
            self.kernel = lambda u: np.exp(-u ** 2 / 2)
        elif deriv_order == 2:
            self.kernel = lambda u: (u ** 2 - 1) * np.exp(-u ** 2 / 2)
        else:
            raise ValueError('Not implemented for derivative of order {}'.format(deriv_order))
        self.deriv_order = deriv_order
        self.h = silverman_bandwidth(data, deriv_order)
        self.datah = data / self.h

    def evaluate(self, x):
        xh = np.array(x).reshape(-1) / self.h
        res = np.zeros(len(xh))
        if len(xh) > len(self.datah):
            for data_ in self.datah:
                res += self.kernel(data_ - xh)
        else:
            for i, x_ in enumerate(xh):
                res[i] = np.sum(self.kernel(self.datah - x_))
        return res * 1.0 / (np.sqrt(2 * np.pi) * self.h ** (1 + self.deriv_order) * len(self.datah))

    def score_samples(self, x):
        return self.evaluate(x)