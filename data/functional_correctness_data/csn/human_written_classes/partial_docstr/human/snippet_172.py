import numpy as np

class min_max:
    """
    Keep only the min/max of streaming values
    """

    def __init__(self):
        self.min = np.inf
        self.max = -np.inf

    def add(self, value: float):
        if value > self.max:
            self.max = value
        if value < self.min:
            self.min = value

    def __iter__(self):
        yield self.min
        yield self.max