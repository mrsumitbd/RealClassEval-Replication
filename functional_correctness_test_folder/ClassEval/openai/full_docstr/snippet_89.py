
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
        >>> tricalculator = TriCalculator()
        >>> tricalculator.factorial(5)
        120
        """
        if a < 0:
            raise ValueError("Factorial is not defined for negative integers")
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
        >>> tricalculator = TriCalculator()
        >>> tricalculator.taylor(60, 50)
        0.5000000000000001
        """
        rad = math.radians(x)
        sum_val = 0.0
        for k in range(n):
            term = ((-1) ** k) * (rad ** (2 * k)) / self.factorial(2 * k)
            sum_val += term
        return sum_val

    def cos(self, x):
        """
        Calculate the cos value of the x-degree angle
        :param x:float
        :return:float
        >>> tricalculator = TriCalculator()
        >>> tricalculator.cos(60)
        0.5
        """
        # Use a sufficiently large number of terms for good accuracy
        return self.taylor(x, 50)

    def sin(self, x):
        """
        Calculate the sin value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator = TriCalculator()
        >>> tricalculator.sin(30)
        0.5
        """
        rad = math.radians(x)
        sum_val = 0.0
        for k in range(50):
            term = ((-1) ** k) * (rad ** (2 * k + 1)) / \
                self.factorial(2 * k + 1)
            sum_val += term
        return sum_val

    def tan(self, x):
        """
        Calculate the tan value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator = TriCalculator()
        >>> tricalculator.tan(45)
        1.0
        """
        cos_val = self.cos(x)
        if abs(cos_val) < 1e-15:
            raise ZeroDivisionError(
                "tan undefined for angles where cos(x) is zero")
        return self.sin(x) / cos_val
