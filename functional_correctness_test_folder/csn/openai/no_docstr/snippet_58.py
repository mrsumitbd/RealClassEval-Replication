
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        """
        Return a binary structuring element in the shape of a disk.
        The disk has a diameter of 2*radius + 1.
        """
        if radius < 0:
            raise ValueError("radius must be non‑negative")
        # Create a grid of coordinates centered at (0,0)
        L = np.arange(-radius, radius + 1)
        X, Y = np.meshgrid(L, L)
        # Mask of points inside the circle
        mask = X**2 + Y**2 <= radius**2
        return mask.astype(np.uint8)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        """
        Return a binary structuring element in the shape of a rectangle.
        """
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        """
        Return a binary structuring element in the shape of a square.
        """
        return MorphologicalStructFactory.get_rectangle(width, width)
