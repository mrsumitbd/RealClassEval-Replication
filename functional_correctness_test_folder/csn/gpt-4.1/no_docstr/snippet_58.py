
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        size = 2 * radius + 1
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x**2 + y**2 <= radius**2
        return mask.astype(np.uint8)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        if width <= 0:
            raise ValueError("Width must be positive")
        return np.ones((width, width), dtype=np.uint8)
