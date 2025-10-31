
import math
import statistics


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
        n = len(data1)
        if n != len(data2):
            raise ValueError("Data sets must be of the same length")
        mean1 = statistics.mean(data1)
        mean2 = statistics.mean(data2)
        std1 = statistics.stdev(data1)
        std2 = statistics.stdev(data2)
        covariance = sum((x - mean1) * (y - mean2)
                         for x, y in zip(data1, data2)) / n
        return covariance / (std1 * std2)

    @staticmethod
    def skewness(data):
        """
        Calculate the skewness of a set of data.
        :param data: The input data list, list.
        :return: The skewness, float.
        >>> DataStatistics4.skewness([1, 2, 5])
        2.3760224064818463

        """
        n = len(data)
        mean = statistics.mean(data)
        std = statistics.stdev(data)
        skew = sum((x - mean) ** 3 for x in data) * \
            n / ((n - 1) * (n - 2) * std ** 3)
        return skew

    @staticmethod
    def kurtosis(data):
        """
        Calculate the kurtosis of a set of data.
        :param data: The input data list, list.
        :return: The kurtosis, float.
        >>> DataStatistics4.kurtosis([1, 20,100])
        -1.5000000000000007

        """
        n = len(data)
        mean = statistics.mean(data)
        std = statistics.stdev(data)
        kurt = sum((x - mean) ** 4 for x in data) * n * (n + 1) / ((n - 1) *
                                                                   (n - 2) * (n - 3) * std ** 4) - 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))
        return kurt

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
        return [1 / (sigma * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((x - mu) / sigma) ** 2) for x in data]
