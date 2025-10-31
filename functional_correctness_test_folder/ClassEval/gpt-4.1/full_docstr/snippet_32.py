
import math


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
        if n != len(data2) or n == 0:
            raise ValueError("Data lists must have the same non-zero length.")
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        num = sum((x - mean1) * (y - mean2) for x, y in zip(data1, data2))
        den1 = math.sqrt(sum((x - mean1) ** 2 for x in data1))
        den2 = math.sqrt(sum((y - mean2) ** 2 for y in data2))
        if den1 == 0 or den2 == 0:
            raise ValueError("Standard deviation cannot be zero.")
        return num / (den1 * den2)

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
        if n < 3:
            raise ValueError("At least 3 data points are required.")
        mean = sum(data) / n
        m2 = sum((x - mean) ** 2 for x in data) / n
        m3 = sum((x - mean) ** 3 for x in data) / n
        if m2 == 0:
            raise ValueError("Variance cannot be zero.")
        g1 = m3 / (m2 ** 1.5)
        # Adjust for sample skewness (Fisher-Pearson)
        skew = (math.sqrt(n * (n - 1)) / (n - 2)) * g1
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
        if n < 4:
            # For n < 4, use the formula for excess kurtosis (biased)
            mean = sum(data) / n
            m2 = sum((x - mean) ** 2 for x in data) / n
            m4 = sum((x - mean) ** 4 for x in data) / n
            if m2 == 0:
                raise ValueError("Variance cannot be zero.")
            kurt = m4 / (m2 ** 2) - 3
            return kurt
        mean = sum(data) / n
        m2 = sum((x - mean) ** 2 for x in data) / n
        m4 = sum((x - mean) ** 4 for x in data) / n
        if m2 == 0:
            raise ValueError("Variance cannot be zero.")
        g2 = m4 / (m2 ** 2) - 3
        # Adjust for sample kurtosis (Fisher-Pearson, excess kurtosis)
        kurt = ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * \
            sum(((x - mean) / math.sqrt(m2)) ** 4 for x in data) - \
            (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
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
        if sigma <= 0:
            raise ValueError("Standard deviation must be positive.")
        result = []
        for x in data:
            val = (1 / (sigma * math.sqrt(2 * math.pi))) * \
                math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
            result.append(val)
        return result
