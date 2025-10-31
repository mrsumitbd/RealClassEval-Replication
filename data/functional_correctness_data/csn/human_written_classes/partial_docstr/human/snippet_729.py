import numpy as np
from scipy.special import beta as betafun

class RefStudentt:
    """
    Reference Student's t distribution for generating random samples, parameterized by a degrees of freedom parameter.

    Parameters:
        beta (float): Shape parameter that influences the degrees of freedom of the Student's t distribution.

    Methods:
        sample(int): Generates a sample from a Student's t distribution.
    """

    def __init__(self, beta):
        self.beta = beta

    def sample(self, n):
        """
        Generates random samples from a Student's t distribution.

        Parameters:
            n (int): Number of samples to generate.

        Returns:
            numpy.ndarray: Array of Student's t random samples.
        """
        dof = 2 * self.beta - 1
        return 1.0 / np.sqrt(dof) * np.random.standard_t(dof, n)