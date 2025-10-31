import numpy as np

class NegativeBinomial:
    """
    Negative binomial variance function

    Parameters
    ----------
    alpha : float
        The ancillary parameter for the negative binomial variance function.
        `alpha` is assumed to be nonstochastic.  The default is 1.

    Methods
    -------
    call
        Returns the negative binomial variance

    Formulas
    --------
    V(mu) = mu + alpha*mu**2

    Notes
    -----
    Alias for NegativeBinomial:
    nbinom = NegativeBinomial()

    A private method _clean trims the data by machine epsilon so that p is
    in (0,inf)
    """

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def _clean(self, p):
        return np.clip(p, FLOAT_EPS, np.inf)

    def __call__(self, mu):
        """
        Negative binomial variance function

        Parameters
        ----------
        mu : array-like
            mean parameters

        Returns
        -------
        variance : array
            variance = mu + alpha*mu**2
        """
        p = self._clean(mu)
        return p + self.alpha * p ** 2

    def deriv(self, mu):
        """
        Derivative of the negative binomial variance function.
        """
        p = self._clean(mu)
        return 1 + 2 * self.alpha * p