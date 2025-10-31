
import math
from collections import Counter
from typing import List, Any


class Statistics3:
    """
    This is a class that implements methods for calculating indicators such as median, mode, correlation matrix, and Z-score in statistics.
    """

    @staticmethod
    def median(data: List[float]) -> float:
        """
        calculates the median of the given list.
        :param data: the given list, list.
        :return: the median of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.median([1, 2, 3, 4])
        2.5
        """
        n = len(data)
        if n == 0:
            raise ValueError("median requires at least one data point")
        sorted_data = sorted(data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
        else:
            return float(sorted_data[mid])

    @staticmethod
    def mode(data: List[Any]) -> List[Any]:
        """
        calculates the mode of the given list.
        :param data: the given list, list.
        :return: the mode of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.mode([1, 2, 3, 3])
        [3]
        """
        if not data:
            return []
        counter = Counter(data)
        max_freq = max(counter.values())
        if max_freq == 1:
            return []
        return [k for k, v in counter.items() if v == max_freq]

    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """
        calculates the correlation of the given list.
        :param x: the given list, list.
        :param y: the given list, list.
        :return: the correlation of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.correlation([1, 2, 3], [4, 5, 6])
        1.0
        """
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        if n < 2:
            raise ValueError("correlation requires at least two data points")
        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)
        cov = sum((xi - mean_x) * (yi - mean_y)
                  for xi, yi in zip(x, y)) / (n - 1)
        std_x = Statistics3.standard_deviation(x)
        std_y = Statistics3.standard_deviation(y)
        if std_x == 0 or std_y == 0:
            return 0.0
        return cov / (std_x * std_y)

    @staticmethod
    def mean(data: List[float]) -> float:
        """
        calculates the mean of the given list.
        :param data: the given list, list.
        :return: the mean of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.mean([1, 2, 3])
        2.0
        """
        if not data:
            raise ValueError("mean requires at least one data point")
        return sum(data) / len(data)

    @staticmethod
    def correlation_matrix(data: List[List[float]]) -> List[List[float]]:
        """
        calculates the correlation matrix of the given list.
        :param data: the given list, list.
        :return: the correlation matrix of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
        """
        if not data:
            return []
        n_vars = len(data)
        matrix = [[0.0] * n_vars for _ in range(n_vars)]
        for i in range(n_vars):
            for j in range(i, n_vars):
                corr = Statistics3.correlation(data[i], data[j])
                matrix[i][j] = corr
                matrix[j][i] = corr
        return matrix

    @staticmethod
    def standard_deviation(data: List[float]) -> float:
        """
        calculates the standard deviation of the given list.
        :param data: the given list, list.
        :return: the standard deviation of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.standard_deviation([1, 2, 3])
        1.0
        """
        n = len(data)
        if n < 2:
            raise ValueError(
                "standard deviation requires at least two data points")
        mean_val = Statistics3.mean(data)
        variance = sum((x - mean_val) ** 2 for x in data) / (n - 1)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data: List[float]) -> List[float]:
        """
        calculates the z-score of the given list.
        :param data: the given list, list.
        :return: the z-score of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.z_score([1, 2, 3, 4])
        [-1.161895003862225, -0.3872983346207417, 0.3872983346207417, 1.161895003862225]
        """
        if not data:
            return []
        mean_val = Statistics3.mean(data)
        std_val = Statistics3.standard_deviation(data)
        if std_val == 0:
            return [0.0 for _ in data]
        return [(x - mean_val) / std_val for x in data]
