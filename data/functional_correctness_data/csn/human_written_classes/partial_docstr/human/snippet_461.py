from fluids.numerics import exp, horner, horner_and_der2, log, sqrt

class Poly_a_alpha:

    def a_alpha_and_derivatives_pure(self, T):
        """Method to calculate `a_alpha` and its first and second
        derivatives given that there is a polynomial equation for
        :math:`\\alpha`.

        .. math::
            a \\alpha = a\\cdot \\text{poly}(T)

        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        a_alphas : list[float]
            Coefficient calculated by EOS-specific method, [J^2/mol^2/Pa]
        da_alpha_dTs : list[float]
            Temperature derivative of coefficient calculated by EOS-specific
            method, [J^2/mol^2/Pa/K]
        d2a_alpha_dT2s : list[float]
            Second temperature derivative of coefficient calculated by
            EOS-specific method, [J^2/mol^2/Pa/K**2]

        """
        res = horner_and_der2(self.alpha_coeffs, T)
        a = self.a
        return (a * res[0], a * res[1], a * res[2])

    def a_alpha_pure(self, T):
        """Method to calculate `a_alpha` given that there is a polynomial
        equation for :math:`\\alpha`.

        .. math::
            a \\alpha = a\\cdot \\text{poly}(T)

        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        a_alpha : float
            Coefficient calculated by EOS-specific method, [J^2/mol^2/Pa]
        """
        return self.a * horner(self.alpha_coeffs, T)