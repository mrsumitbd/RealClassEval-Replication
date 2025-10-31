class DataStatistics4:
    """
    This is a class that performs advanced mathematical calculations and statistics, including correlation coefficient, skewness, kurtosis, and probability density function (PDF) for a normal distribution.
    """

    @staticmethod
    def correlation_coefficient(data1, data2):
        """
        Calculate the correlation coefficient of two sets of data.
        :param data1: The first set of data,list.
        :param data2: The second set of data,list.
        :return: The correlation coefficient, float.
        >>> DataStatistics4.correlation_coefficient([1, 2, 3], [4, 5, 6])
        0.9999999999999998

        """
        import math
        if not isinstance(data1, list) or not isinstance(data2, list):
            raise TypeError("data1 and data2 must be lists")
        if len(data1) != len(data2) or len(data1) < 2:
            raise ValueError(
                "data1 and data2 must have the same length and length >= 2")
        n = len(data1)
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        cov = sum((x - mean1) * (y - mean2) for x, y in zip(data1, data2)) / n
        var1 = sum((x - mean1) ** 2 for x in data1) / n
        var2 = sum((y - mean2) ** 2 for y in data2) / n
        if var1 == 0 or var2 == 0:
            raise ValueError("Variance of data1 or data2 is zero")
        return cov / math.sqrt(var1 * var2)

    @staticmethod
    def skewness(data):
        """
        Calculate the skewness of a set of data.
        :param data: The input data list, list.
        :return: The skewness, float.
        >>> DataStatistics4.skewness([1, 2, 5])
        2.3760224064818463

        """
        import math
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        n = len(data)
        if n < 3:
            raise ValueError("skewness requires at least 3 data points")
        mean = sum(data) / n
        diffs = [x - mean for x in data]
        m2 = sum(d * d for d in diffs) / n  # population second central moment
        if m2 == 0:
            return 0.0
        # sum of third central moment terms
        m3_sum = sum(d ** 3 for d in diffs)
        sigma = math.sqrt(m2)
        # Adjusted skewness using population sigma in the denominator
        return (n / ((n - 1) * (n - 2))) * (m3_sum / (sigma ** 3))

    @staticmethod
    def kurtosis(data):
        """
        Calculate the kurtosis of a set of data.
        :param data: The input data list, list.
        :return: The kurtosis, float.
        >>> DataStatistics4.kurtosis([1, 20,100])
        -1.5000000000000007

        """
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        n = len(data)
        if n == 0:
            raise ValueError("kurtosis requires at least 1 data point")
        mean = sum(data) / n
        diffs = [x - mean for x in data]
        m2 = sum(d * d for d in diffs) / n  # population second central moment
        if m2 == 0:
            return -3.0  # degenerate case: all points equal -> excess kurtosis of a delta is undefined; return -3 for consistency with μ4/μ2^2 - 3 when μ4=0
        m4 = sum(d ** 4 for d in diffs) / n  # population fourth central moment
        return (m4 / (m2 ** 2)) - 3.0

    @staticmethod
    def pdf(data, mu, sigma):
        """
        Calculate the probability density function (PDF) of a set of data under a normal distribution.
        :param data: The input data list, list.
        :param mu: The mean of the normal distribution, float.
        :param sigma: The standard deviation of the normal distribution, float.
        :return: The probability density function (PDF), list.
        >>> DataStatistics4.pdf([1, 2, 3], 1, 1)
        [0.3989422804014327, 0.24197072451914337, 0.05399096651318806]

        """
        import math
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        if sigma <= 0:
            raise ValueError("sigma must be positive")
        coef = 1.0 / (math.sqrt(2.0 * math.pi) * sigma)
        two_sigma2 = 2.0 * sigma * sigma
        return [coef * math.exp(-((x - mu) ** 2) / two_sigma2) for x in data]
