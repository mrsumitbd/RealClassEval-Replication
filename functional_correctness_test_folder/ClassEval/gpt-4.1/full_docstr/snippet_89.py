
import math


class TriCalculator:
    """
    The class allows to calculate trigonometric values, including cosine, sine, and tangent, using Taylor series approximations.
    """

    def __init__(self):
        pass

    def factorial(self, a):
        """
        Calculate the factorial of a
        :param a: int
        :return: int
        >>> tricalculator.factorial(5)
        120
        """
        if a == 0 or a == 1:
            return 1
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
        rad = x * math.pi / 180
        result = 0.0
        for k in range(n):
            term = ((-1) ** k) * (rad ** (2 * k)) / self.factorial(2 * k)
            result += term
        return result

    def cos(self, x):
        """
        Calculate the cos value of the x-degree angle
        :param x:float
        :return:float
        >>> tricalculator = TriCalculator()
        >>> tricalculator.cos(60)
        0.5
        """
        # Use enough terms for good accuracy
        return round(self.taylor(x, 20), 10)

    def sin(self, x):
        """
        Calculate the sin value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator.sin(30)
        0.5
        """
        rad = x * math.pi / 180
        result = 0.0
        for k in range(20):
            term = ((-1) ** k) * (rad ** (2 * k + 1)) / \
                self.factorial(2 * k + 1)
            result += term
        return round(result, 10)

    def tan(self, x):
        """
        Calculate the tan value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator.tan(45)
        1.0
        """
        cos_val = self.cos(x)
        if abs(cos_val) < 1e-12:
            raise ValueError(
                "tan is undefined for this angle (cos(x) is zero)")
        sin_val = self.sin(x)
        return round(sin_val / cos_val, 10)
