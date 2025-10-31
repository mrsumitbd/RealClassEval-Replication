class TriCalculator:
    """
    The class allows to calculate trigonometric values, including cosine, sine, and tangent, using Taylor series approximations.
    """

    def __init__(self):
        pass

    def cos(self, x):
        """
        Calculate the cos value of the x-degree angle
        :param x:float
        :return:float
        >>> tricalculator = TriCalculator()
        >>> tricalculator.cos(60)
        0.5
        """
        rad = self._to_radians(x)
        # Use Taylor series for cosine with sufficient terms
        n_terms = 25
        result = 1.0
        term = 1.0
        for k in range(1, n_terms + 1):
            term *= -rad * rad / ((2 * k - 1) * (2 * k))
            result += term
        return self._rounded(result)

    def factorial(self, a):
        """
        Calculate the factorial of a
        :param a: int
        :return: int
        >>> tricalculator.factorial(5)
        120
        """
        if not isinstance(a, int):
            raise TypeError("factorial input must be an integer")
        if a < 0:
            raise ValueError("factorial is not defined for negative numbers")
        result = 1
        for i in range(2, a + 1):
            result *= i
        return result

    def taylor(self, x, n):
        """
        Finding the n-order Taylor expansion value of cos (x/180 * pi)
        :param x: int
        :param n: int
        :return: float
        >>> tricalculator.taylor(60, 50)
        0.5000000000000001
        """
        rad = self._to_radians(x)
        result = 1.0
        term = 1.0
        for k in range(1, n + 1):
            term *= -rad * rad / ((2 * k - 1) * (2 * k))
            result += term
        return result

    def sin(self, x):
        """
        Calculate the sin value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator.sin(30)
        0.5
        """
        rad = self._to_radians(x)
        n_terms = 25
        result = rad
        term = rad
        for k in range(1, n_terms + 1):
            term *= -rad * rad / ((2 * k) * (2 * k + 1))
            result += term
        return self._rounded(result)

    def tan(self, x):
        """
        Calculate the tan value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator.tan(45)
        1.0
        """
        c = self.cos(x)
        s = self.sin(x)
        eps = 1e-15
        if abs(c) < eps:
            return float('inf') if s >= 0 else float('-inf')
        return self._rounded(s / c)

    def _to_radians(self, degrees):
        import math
        # Normalize degrees to improve series convergence
        d = degrees % 360.0
        return d * math.pi / 180.0

    def _rounded(self, value, ndigits=12):
        # Round to stabilize common angles (e.g., 30, 45, 60) for doctests
        r = round(value, ndigits)
        # Avoid negative zero
        return 0.0 if r == -0.0 else r
