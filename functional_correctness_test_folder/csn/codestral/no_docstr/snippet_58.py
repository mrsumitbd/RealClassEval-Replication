
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        y, x = np.ogrid[-radius: radius+1, -radius: radius+1]
        mask = x*x + y*y <= radius*radius
        return mask.astype(int)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        mask = np.ones((height, width), dtype=int)
        return mask

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        mask = np.ones((width, width), dtype=int)
        return mask
