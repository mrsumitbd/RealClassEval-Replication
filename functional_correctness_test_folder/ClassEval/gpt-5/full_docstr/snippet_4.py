from itertools import permutations


class ArrangementCalculator:
    """
    The Arrangement class provides permutation calculations and selection operations for a given set of data elements.
    """

    def __init__(self, datas):
        """
        Initializes the ArrangementCalculator object with a list of datas.
        :param datas: List, the data elements to be used for arrangements.
        """
        self.datas = list(datas)

    @staticmethod
    def count(n, m=None):
        """
        Counts the number of arrangements by choosing m items from n items (permutations).
        If m is not provided or n equals m, returns factorial(n).
        :param n: int, the total number of items.
        :param m: int, the number of items to be chosen (default=None).
        :return: int, the count of arrangements.
        >>> ArrangementCalculator.count(5, 3)
        60

        """
        if not isinstance(n, int) or (m is not None and not isinstance(m, int)):
            raise TypeError("n and m must be integers")
        if n < 0:
            raise ValueError("n must be non-negative")
        if m is None:
            m = n
        if m < 0 or m > n:
            raise ValueError("m must be between 0 and n inclusive")
        if m == 0:
            return 1
        if m == n:
            return ArrangementCalculator.factorial(n)
        result = 1
        for k in range(n - m + 1, n + 1):
            result *= k
        return result

    @staticmethod
    def count_all(n):
        """
        Counts the total number of all possible arrangements by choosing at least 1 item and at most n items from n items.
        :param n: int, the total number of items.
        :return: int, the count of all arrangements.
        >>> ArrangementCalculator.count_all(4)
        64

        """
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 0:
            raise ValueError("n must be non-negative")
        total = 0
        for k in range(1, n + 1):
            total += ArrangementCalculator.count(n, k)
        return total

    def select(self, m=None):
        """
        Generates a list of arrangements by selecting m items from the internal datas.
        If m is not provided, selects all items.
        :param m: int, the number of items to be chosen (default=None).
        :return: List, a list of arrangements.
        >>> ac = ArrangementCalculator([1, 2, 3, 4])
        >>> ac.select(2)
        [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]]

        """
        n = len(self.datas)
        if m is None:
            m = n
        if not isinstance(m, int):
            raise TypeError("m must be an integer")
        if m < 0 or m > n:
            raise ValueError(
                "m must be between 0 and the number of datas inclusive")
        return [list(p) for p in permutations(self.datas, m)]

    def select_all(self):
        """
        Generates a list of all arrangements by selecting at least 1 item and at most the number of internal datas.
        :return: List, a list of all arrangements.
        >>> ac = ArrangementCalculator([1, 2, 3])
        >>> ac.select_all()
        [[1], [2], [3], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

        """
        result = []
        n = len(self.datas)
        for k in range(1, n + 1):
            result.extend([list(p) for p in permutations(self.datas, k)])
        return result

    @staticmethod
    def factorial(n):
        """
        Calculates the factorial of a given number.
        :param n: int, the number to calculate the factorial.
        :return: int, the factorial of the given number.
        >>> ArrangementCalculator.factorial(4)
        24

        """
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 0:
            raise ValueError("n must be non-negative")
        result = 1
        for k in range(2, n + 1):
            result *= k
        return result
