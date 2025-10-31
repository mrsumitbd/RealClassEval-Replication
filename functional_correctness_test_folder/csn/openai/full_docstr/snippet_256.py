
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
        '''
        Default variance function
        Parameters
        -----------
        mu : array-like
            mean parameters
        Returns
        -------
        v : array
            ones(mu.shape)
        '''
        mu_arr = np.asarray(mu)
        return np.ones_like(mu_arr)

    def deriv(self, mu):
        '''
        Derivative of the variance function v'(mu)
        '''
        mu_arr = np.asarray(mu)
        return np.zeros_like(mu_arr)


# Alias
constant = VarianceFunction()
