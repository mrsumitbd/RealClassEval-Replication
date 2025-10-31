
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        diameter = 2 * radius + 1
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x**2 + y**2 <= radius**2
        struct = np.zeros((diameter, diameter), dtype=np.uint8)
        struct[mask] = 1
        return struct

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        return np.ones((width, width), dtype=np.uint8)
