import numpy as np

class Partition:

    def __init__(self, slices, shuffle=True, seed=None):
        self._slices = slices
        self._total_length = 0
        for item in slices:
            self._total_length += item.length
        self._index = 0
        if shuffle:
            self._elements = _random_state(seed).permutation(self._total_length)
        else:
            self._elements = np.arange(0, self._total_length)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == self._total_length:
            raise StopIteration()
        index = self._elements[self._index]
        for item in self._slices:
            if index >= item.length:
                index -= item.length
                continue
            self._index += 1
            return (item.data_set_name, item.start_index + index, item.data[index])

    def has_next(self):
        return self._index < self._total_length