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
            raise ValueError("Data list is empty")
        total = sum(data)
        count = len(data)
        return round(total / count, 2)

    def median(self, data):
        """
        Calculate the median of a group of data, accurate to two digits after the Decimal separator
        :param data:list, data list
        :return:float, the median value
        >>> ds = DataStatistics()
        >>> ds.median([2, 5, 1, 3, 4])
        3.00
        """
        if not data:
            raise ValueError("Data list is empty")
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            median_val = sorted_data[mid]
        else:
            median_val = (sorted_data[mid - 1] + sorted_data[mid]) / 2
        return round(median_val, 2)

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
            raise ValueError("Data list is empty")
        freq = {}
        for item in data:
            freq[item] = freq.get(item, 0) + 1
        max_count = max(freq.values())
        modes = [k for k, v in freq.items() if v == max_count]
        if len(modes) == 1:
            return modes[0]
        return sorted(modes)
