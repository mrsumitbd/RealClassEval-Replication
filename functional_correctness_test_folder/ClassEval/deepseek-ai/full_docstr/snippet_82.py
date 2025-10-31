
import math


class Statistics3:
    """
    This is a class that implements methods for calculating indicators such as median, mode, correlation matrix, and Z-score in statistics.
    """

    @staticmethod
    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            return sorted_data[n // 2]
        else:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    @staticmethod
    def mode(data):
        frequency = {}
        for num in data:
            frequency[num] = frequency.get(num, 0) + 1
        max_freq = max(frequency.values())
        modes = [num for num, freq in frequency.items() if freq == max_freq]
        return sorted(modes)

    @staticmethod
    def correlation(x, y):
        n = len(x)
        if n != len(y) or n == 0:
            return 0.0
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        if std_x == 0 or std_y == 0:
            return 0.0
        return cov / (std_x * std_y)

    @staticmethod
    def mean(data):
        return sum(data) / len(data) if len(data) > 0 else 0.0

    @staticmethod
    def correlation_matrix(data):
        n = len(data)
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                matrix[i][j] = Statistics3.correlation(data[i], data[j])
        return matrix

    @staticmethod
    def standard_deviation(data):
        if len(data) == 0:
            return 0.0
        mean = Statistics3.mean(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data):
        if len(data) == 0:
            return []
        mean = Statistics3.mean(data)
        std = Statistics3.standard_deviation(data)
        if std == 0:
            return [0.0 for _ in data]
        return [(x - mean) / std for x in data]
