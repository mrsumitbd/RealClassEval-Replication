import numpy as np

class Binomial:
    """
    Binomial variance function

    Parameters
    ----------
    n : int, optional
        The number of trials for a binomial variable.  The default is 1 for
        p in (0,1)

    Methods
    -------
    call
        Returns the binomial variance

    Formulas
    --------
    V(mu) = p * (1 - p) * n

    where p = mu / n

    Notes
    -----
    Alias for Binomial:
    binary = Binomial()

    A private method _clean trims the data by machine epsilon so that p is
    in (0,1)
    """

    def __init__(self, n=1):
        self.n = n

    def _clean(self, p):
        return np.clip(p, FLOAT_EPS, 1 - FLOAT_EPS)

    def __call__(self, mu):
        """
        Binomial variance function

        Parameters
        -----------
        mu : array-like
            mean parameters

        Returns
        -------
        variance : array
           variance = mu/n * (1 - mu/n) * self.n
        """
        p = self._clean(mu / self.n)
        return p * (1 - p) * self.n

    def deriv(self, mu):
        """
        Derivative of the variance function v'(mu)
        """
        from statsmodels.tools.numdiff import approx_fprime_cs
        return np.diag(approx_fprime_cs(mu, self))