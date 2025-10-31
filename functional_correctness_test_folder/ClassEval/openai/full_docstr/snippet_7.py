class AvgPartition:
    """
    This is a class that partitions the given list into different blocks by specifying the number of partitions,
    with each block having a uniformly distributed length.
    """

    def __init__(self, lst, limit):
        """
        Initialize the class with the given list and the number of partitions, and check if the number of partitions is greater than 0.
        """
        if limit <= 0:
            raise ValueError("Number of partitions must be greater than 0")
        self.lst = lst
        self.limit = limit

    def setNum(self):
        """
        Calculate the size of each block and the remainder of the division.
        :return: the size of each block and the remainder of the division, tuple.
        >>> a = AvgPartition([1, 2, 3, 4], 2)
        >>> a.setNum()
        (2, 0)
        """
        n = len(self.lst)
        block_size = n // self.limit
        remainder = n % self.limit
        return block_size, remainder

    def get(self, index):
        """
        calculate the size of each block and the remainder of the division, and calculate the corresponding start and end positions based on the index of the partition.
        :param index: the index of the partition,int.
        :return: the corresponding block, list.
        >>> a = AvgPartition([1, 2, 3, 4], 2)
        >>> a.get(0)
        [1, 2]
        """
        if not (0 <= index < self.limit):
            raise IndexError("Partition index out of range")

        block_size, remainder = self.setNum()

        # Determine the size of this block
        extra = 1 if index < remainder else 0
        size = block_size + extra

        # Compute start index
        start = index * block_size + min(index, remainder)
        end = start + size
        return self.lst[start:end]
