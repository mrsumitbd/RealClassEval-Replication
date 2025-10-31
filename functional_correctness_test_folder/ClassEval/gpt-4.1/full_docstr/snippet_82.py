
class Statistics3:
    """
    This is a class that implements methods for calculating indicators such as median, mode, correlation matrix, and Z-score in statistics.
    """

    @staticmethod
    def median(data):
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
            raise ValueError("data must not be empty")
        sorted_data = sorted(data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
        else:
            return float(sorted_data[mid])

    @staticmethod
    def mode(data):
        """
        calculates the mode of the given list.
        :param data: the given list, list.
        :return: the mode of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.mode([1, 2, 3, 3])
        [3]
        """
        if not data:
            raise ValueError("data must not be empty")
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        return sorted([k for k, v in counts.items() if v == max_count])

    @staticmethod
    def correlation(x, y):
        """
        calculates the correlation of the given list.
        :param x: the given list, list.
        :param y: the given list, list.
        :return: the correlation of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.correlation([1, 2, 3], [4, 5, 6])
        1.0
        """
        if len(x) != len(y) or len(x) == 0:
            raise ValueError("x and y must be of same non-zero length")
        n = len(x)
        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)
        std_x = Statistics3.standard_deviation(x)
        std_y = Statistics3.standard_deviation(y)
        if std_x == 0 or std_y == 0:
            raise ValueError(
                "Standard deviation cannot be zero for correlation")
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        return cov / (std_x * std_y)

    @staticmethod
    def mean(data):
        """
        calculates the mean of the given list.
        :param data: the given list, list.
        :return: the mean of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.mean([1, 2, 3])
        2.0
        """
        if not data:
            raise ValueError("data must not be empty")
        return sum(data) / float(len(data))

    @staticmethod
    def correlation_matrix(data):
        """
        calculates the correlation matrix of the given list.
        :param data: the given list, list.
        :return: the correlation matrix of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
        """
        if not data or not all(len(row) == len(data[0]) for row in data):
            raise ValueError(
                "data must be a non-empty list of lists of equal length")
        n = len(data)
        result = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(Statistics3.correlation(data[i], data[j]))
            result.append(row)
        return result

    @staticmethod
    def standard_deviation(data):
        """
        calculates the standard deviation of the given list.
        :param data: the given list, list.
        :return: the standard deviation of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.standard_deviation([1, 2, 3])
        1.0
        """
        if not data:
            raise ValueError("data must not be empty")
        mean = Statistics3.mean(data)
        n = len(data)
        variance = sum((x - mean) ** 2 for x in data) / n
        return variance ** 0.5

    @staticmethod
    def z_score(data):
        """
        calculates the z-score of the given list.
        :param data: the given list, list.
        :return: the z-score of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.z_score([1, 2, 3, 4])
        [-1.161895003862225, -0.3872983346207417, 0.3872983346207417, 1.161895003862225]
        """
        if not data:
            raise ValueError("data must not be empty")
        mean = Statistics3.mean(data)
        std = Statistics3.standard_deviation(data)
        if std == 0:
            raise ValueError("Standard deviation cannot be zero for z-score")
        return [(x - mean) / std for x in data]
