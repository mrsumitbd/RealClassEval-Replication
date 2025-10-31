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
        if not data:
            raise ValueError("data must not be empty")
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            return float(sorted_data[mid])
        else:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0

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
        if not counts:
            return []
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        try:
            modes.sort()
        except TypeError:
            pass
        return modes

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
        if x is None or y is None:
            raise ValueError("x and y must not be None")
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        if n < 2:
            raise ValueError("x and y must have length at least 2")
        mx = Statistics3.mean(x)
        my = Statistics3.mean(y)
        sx = Statistics3.standard_deviation(x)
        sy = Statistics3.standard_deviation(y)
        if sx == 0 or sy == 0:
            return 0.0
        cov_num = 0.0
        for xi, yi in zip(x, y):
            cov_num += (xi - mx) * (yi - my)
        # sample covariance uses (n-1)
        cov = cov_num / (n - 1)
        return cov / (sx * sy)

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
        return float(sum(data)) / len(data)

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
        if not data:
            raise ValueError("data must not be empty")
        lengths = [len(series) for series in data]
        if any(l != lengths[0] for l in lengths):
            raise ValueError("all series must have the same length")
        if lengths[0] < 2:
            raise ValueError("each series must have length at least 2")
        m = len(data)
        result = []
        for i in range(m):
            row = []
            for j in range(m):
                if i == j:
                    row.append(1.0)
                else:
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
        n = len(data)
        if n < 2:
            raise ValueError(
                "data must contain at least two elements for standard deviation")
        m = Statistics3.mean(data)
        var_sum = 0.0
        for x in data:
            d = x - m
            var_sum += d * d
        var = var_sum / (n - 1)
        return var ** 0.5

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
        mean_val = Statistics3.mean(data)
        std_val = Statistics3.standard_deviation(data)
        if std_val == 0:
            return [0.0 for _ in data]
        return [(x - mean_val) / std_val for x in data]
