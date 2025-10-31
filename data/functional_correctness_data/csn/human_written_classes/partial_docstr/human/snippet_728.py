import numpy as np
from scipy.special import beta as betafun

class RefBeta:
    """
    Reference Beta distribution for generating random samples, parameterized by a shape parameter.

    Parameters:
        beta (float): Shape parameter for both alpha and beta of the Beta distribution.

    Methods:
        sample(int): Generates a sample from a Beta distribution.
    """

    def __init__(self, beta):
        self.beta = beta

    def sample(self, n):
        """
        Generates random samples from a Beta distribution.

        Parameters:
            n (int): Number of samples to generate.

        Returns:
            numpy.ndarray: Array of Beta random samples.
        """
        return np.random.beta(self.beta, self.beta, n)