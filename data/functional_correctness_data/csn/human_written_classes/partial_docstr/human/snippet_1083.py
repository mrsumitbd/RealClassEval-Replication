import numpy as np

class Power:
    """
    Power variance function

    Parameters
    ----------
    power : float
        exponent used in power variance function

    Methods
    -------
    call
        Returns the power variance

    Formulas
    --------
    V(mu) = numpy.fabs(mu)**power

    Notes
    -----
    Aliases for Power:
    mu = Power()
    mu_squared = Power(power=2)
    mu_cubed = Power(power=3)
    """

    def __init__(self, power=1.0):
        self.power = power

    def __call__(self, mu):
        """
        Power variance function

        Parameters
        ----------
        mu : array-like
            mean parameters

        Returns
        -------
        variance : array
            numpy.fabs(mu)**self.power
        """
        return np.power(np.fabs(mu), self.power)

    def deriv(self, mu):
        """
        Derivative of the variance function v'(mu)
        """
        from statsmodels.tools.numdiff import approx_fprime_cs
        from statsmodels.tools.numdiff import approx_fprime
        return np.diag(approx_fprime(mu, self))