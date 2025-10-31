
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        '''
        :param radius: Radius of disk
        :return: The structuring element where elements of the neighborhood are 1 and 0 otherwise.
        '''
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        size = 2 * radius + 1
        y, x = np.ogrid[-radius:radius+1, -radius:radius+1]
        mask = x**2 + y**2 <= radius**2
        return mask.astype(np.uint8)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        '''
        :param width: Width of rectangle
        :param height: Height of rectangle
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        '''
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers")
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        '''
        :param width: Size of square
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        '''
        if width <= 0:
            raise ValueError("Width must be a positive integer")
        return np.ones((width, width), dtype=np.uint8)
