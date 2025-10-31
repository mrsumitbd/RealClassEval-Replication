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
            raise ValueError("data must not be empty")
        return round(sum(data) / len(data), 2)

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
            raise ValueError("data must not be empty")
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            return round(float(sorted_data[mid]), 2)
        else:
            return round((sorted_data[mid - 1] + sorted_data[mid]) / 2.0, 2)

    def mode(self, data):
        """
        Calculate the mode of a set of data
        :param data:list, data list
        :return:list, the mode(s)
        >>> ds = DataStatistics()
        >>> ds.mode([2, 2, 3, 3, 4])
        [2, 3]
        """
        if not data:
            raise ValueError("data must not be empty")
        from collections import Counter

        counts = Counter(data)
        if not counts:
            return []
        max_count = max(counts.values())
        modes = [val for val, cnt in counts.items() if cnt == max_count]
        return sorted(modes)
