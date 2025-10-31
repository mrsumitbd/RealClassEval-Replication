import numpy as np

class DataMapper:
    """Convert packed integer data into physical units."""
    RANGE_FOLD = float('nan')
    MISSING = float('nan')

    def __init__(self, num=256):
        self.lut = np.full(num, self.MISSING, dtype=float)

    def __call__(self, data):
        """Convert the values."""
        return self.lut[data]