
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        """
        Return a binary structuring element of a disk with the given radius.
        The element is a 2D array of shape (2*radius+1, 2*radius+1) where
        elements inside the disk are 1 and outside are 0.
        """
        if radius < 0:
            raise ValueError("radius must be non‑negative")
        size = 2 * radius + 1
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x**2 + y**2 <= radius**2
        return mask.astype(np.uint8)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        """
        Return a rectangular structuring element of the given width and height.
        The element is a 2D array of shape (height, width) filled with 1s.
        """
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        """
        Return a square structuring element of the given width.
        The element is a 2D array of shape (width, width) filled with 1s.
        """
        if width <= 0:
            raise ValueError("width must be positive")
        return np.ones((width, width), dtype=np.uint8)
