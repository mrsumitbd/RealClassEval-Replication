
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        diameter = 2 * radius + 1
        struct = np.zeros((diameter, diameter), dtype=np.uint8)
        center = radius
        for i in range(diameter):
            for j in range(diameter):
                if (i - center)**2 + (j - center)**2 <= radius**2:
                    struct[i, j] = 1
        return struct

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        return np.ones((width, width), dtype=np.uint8)
