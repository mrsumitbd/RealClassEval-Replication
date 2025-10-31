
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x**2 + y**2 <= radius**2
        return mask.astype(np.uint8)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        return np.ones((width, width), dtype=np.uint8)
