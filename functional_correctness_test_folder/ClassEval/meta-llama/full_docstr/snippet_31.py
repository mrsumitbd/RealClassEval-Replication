
import numpy as np


class DataStatistics2:
    """
    This is a class for performing data statistics, supporting to get the sum, minimum, maximum, variance, standard deviation, and correlation of a given dataset.
    """

    def __init__(self, data):
        """
        Initialize Data List
        :param data:list
        """
        self.data = np.array(data)

    def get_sum(self):
        """
        Calculate the sum of data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_sum()
        10
        """
        return np.sum(self.data)

    def get_min(self):
        """
        Calculate the minimum value in the data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_min()
        1
        """
        return np.min(self.data)

    def get_max(self):
        """
        Calculate the maximum value in the data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_max()
        4
        """
        return np.max(self.data)

    def get_variance(self):
        """
        Calculate variance, accurate to two digits after the Decimal separator
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_variance()
        1.25
        """
        return round(np.var(self.data), 2)

    def get_std_deviation(self):
        """
        Calculate standard deviation, accurate to two digits after the Decimal separator
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_std_deviation()
        1.12
        """
        return round(np.std(self.data), 2)

    def get_correlation(self):
        """
        Calculate correlation
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_correlation()
        1.0
        """
        x = np.arange(len(self.data))
        corr_coef = np.corrcoef(x, self.data)[0, 1]
        return corr_coef


# Example usage
if __name__ == "__main__":
    ds2 = DataStatistics2([1, 2, 3, 4])
    print(ds2.get_sum())
    print(ds2.get_min())
    print(ds2.get_max())
    print(ds2.get_variance())
    print(ds2.get_std_deviation())
    print(ds2.get_correlation())
