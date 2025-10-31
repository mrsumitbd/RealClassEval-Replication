
from typing import List, Union
from statistics import median as stats_median, multimode


class DataStatistics:
    """
    This is a class for performing data statistics, supporting to calculate the mean, median, and mode of a given data set.
    """

    def mean(self, data: List[Union[int, float]]) -> float:
        """
        Calculate the average value of a group of data, accurate to two digits after the Decimal separator
        :param data:list, data list
        :return:float, the mean value
        >>> ds = DataStatistics()
        >>> ds.mean([1, 2, 3, 4, 5])
        3.00
        """
        if not data:
            raise ValueError("Cannot calculate mean of empty data")
        return round(sum(data) / len(data), 2)

    def median(self, data: List[Union[int, float]]) -> float:
        """
        Calculate the median of a group of data, accurate to two digits after the Decimal separator
        :param data:list, data list
        :return:float, the median value
        >>> ds = DataStatistics()
        >>> ds.median([2, 5, 1, 3, 4])
        3.00
        """
        if not data:
            raise ValueError("Cannot calculate median of empty data")
        return round(stats_median(data), 2)

    def mode(self, data: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        Calculate the mode of a set of data
        :param data:list, data list
        :return:float, the mode
        >>> ds = DataStatistics()
        >>> ds.mode([2, 2, 3, 3, 4])
        [2, 3]
        """
        if not data:
            raise ValueError("Cannot calculate mode of empty data")
        return multimode(data)
