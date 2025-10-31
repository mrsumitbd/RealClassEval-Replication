import numpy as np
from HARK.interpolation import BilinearInterp, ConstantFunction, CubicInterp, LinearInterp, MargValueFuncCRRA, ValueFuncCRRA

class ChiFromOmegaFunction:
    """
    A class for representing a function that takes in values of omega = EndOfPrdvP / aNrm
    and returns the corresponding optimal chi = cNrm / aNrm. The only parameters
    that matter for this transformation are the coefficient of relative risk
    aversion rho and the share of wealth in the Cobb-Douglas aggregator delta.

    Parameters
    ----------
    rho : float
        Coefficient of relative risk aversion.
    delta : float
        Share for wealth in the Cobb-Douglas aggregator in CRRA utility function.
    N : int, optional
        Number of interpolating gridpoints to use (default 501).
    z_bound : float, optional
        Absolute value on the auxiliary variable z's boundary (default 15).
        z represents values that are input into a logit transformation
        scaled by the upper bound of chi, which yields chi values.
    """

    def __init__(self, CRRA, WealthShare, N=501, z_bound=15):
        self.CRRA = CRRA
        self.WealthShare = WealthShare
        self.N = N
        self.z_bound = z_bound
        self.update()

    def f(self, x):
        """
        Define the relationship between chi and omega, and evaluate on the vector
        """
        return x ** (1 - self.WealthShare) * ((1 - self.WealthShare) * x ** (-self.WealthShare) - self.WealthShare * x ** (1 - self.WealthShare)) ** (-1 / self.CRRA)

    def update(self):
        """
        Construct the underlying interpolation of log(omega) on z.
        """
        chi_limit = (1.0 - self.WealthShare) / self.WealthShare
        z_vec = np.linspace(-self.z_bound, self.z_bound, self.N)
        exp_z = np.exp(z_vec)
        chi_vec = chi_limit * exp_z / (1 + exp_z)
        omega_vec = self.f(chi_vec)
        log_omega_vec = np.log(omega_vec)
        zFromLogOmegaFunc = LinearInterp(log_omega_vec, z_vec, lower_extrap=True)
        self.func = zFromLogOmegaFunc
        self.limit = chi_limit

    def __call__(self, omega):
        """
        Calculate optimal values of chi = cNrm / aNrm from values of omega.

        Parameters
        ----------
        omega : np.array
            One or more values of omega = EndOfPrdvP / aNrm.

        Returns
        -------
        chi : np.array
            Identically shaped array with optimal chi values.
        """
        z = self.func(np.log(omega))
        exp_z = np.exp(z)
        chi = self.limit * exp_z / (1 + exp_z)
        return np.nan_to_num(chi)