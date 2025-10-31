import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        if not isinstance(radius, int):
            raise TypeError("radius must be an integer")
        if radius < 0:
            raise ValueError("radius must be >= 0")
        if radius == 0:
            return np.ones((1, 1), dtype=bool)
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x*x + y*y <= radius*radius
        return mask.astype(bool)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be integers")
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be > 0")
        return np.ones((height, width), dtype=bool)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        if width <= 0:
            raise ValueError("width must be > 0")
        return np.ones((width, width), dtype=bool)
