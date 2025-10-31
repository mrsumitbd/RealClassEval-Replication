
class DataStatistics:
    """
    This is a class for performing data statistics, supporting to calculate the mean, median, and mode of a given data set.
    """

    def mean(self, data):
        """
        Calculate the average value of a group of data, accurate to two digits after the Decimal separator
        :param data:list, data list
        :return:float, the mean value
        >>> ds = DataStatistics()
        >>> ds.mean([1, 2, 3, 4, 5])
        3.00
        """
        if not data:
            return 0.00
        avg = sum(data) / len(data)
        return float(f"{avg:.2f}")

    def median(self, data):
        """
        Calculate the median of a group of data, accurate to two digits after the Decimal separator
        :param data:list, data list
        :return:float, the median value
        >>> ds = DataStatistics()
        >>> ds.median([2, 5, 1, 3, 4])
        3.00
        """
        n = len(data)
        if n == 0:
            return 0.00
        sorted_data = sorted(data)
        mid = n // 2
        if n % 2 == 1:
            med = sorted_data[mid]
        else:
            med = (sorted_data[mid - 1] + sorted_data[mid]) / 2
        return float(f"{med:.2f}")

    def mode(self, data):
        """
        Calculate the mode of a set of data
        :param data:list, data list
        :return:float, the mode
        >>> ds = DataStatistics()
        >>> ds.mode([2, 2, 3, 3, 4])
        [2, 3]
        """
        if not data:
            return []
        from collections import Counter
        count = Counter(data)
        max_freq = max(count.values())
        modes = [k for k, v in count.items() if v == max_freq]
        if len(modes) == 1:
            return modes[0]
        else:
            return sorted(modes)
