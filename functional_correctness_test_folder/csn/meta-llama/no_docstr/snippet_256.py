
import numpy as np


class VarianceFunction:
    '''
    Relates the variance of a random variable to its mean. Defaults to 1.
    Methods
    -------
    call
        Returns an array of ones that is the same shape as `mu`
    Notes
    -----
    After a variance function is initialized, its call method can be used.
    Alias for VarianceFunction:
    constant = VarianceFunction()
    See also
    --------
    statsmodels.family.family
    '''

    def __call__(self, mu):
        return np.ones_like(mu)

    def deriv(self, mu):
        return np.zeros_like(mu)


# Example usage:
constant = VarianceFunction()
mu = np.array([1, 2, 3])
print(constant(mu))  # Output: [1 1 1]
print(constant.deriv(mu))  # Output: [0 0 0]
