import numpy as np


class MorphologicalStructFactory:
    '''
    Factory methods for generating morphological structuring elements
    '''
    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        '''
        :param radius: Radius of disk
        :return: The structuring element where elements of the neighborhood are 1 and 0 otherwise.
        '''
        if not isinstance(radius, int) or radius < 0:
            raise ValueError("radius must be a non-negative integer")
        size = 2 * radius + 1
        yy, xx = np.ogrid[-radius:radius + 1, -radius:radius + 1]
        mask = (xx * xx + yy * yy) <= radius * radius
        return mask.astype(np.uint8)

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        '''
        :param width: Width of rectangle
        :param height: Height of rectangle
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        '''
        if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers")
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        '''
        :param width: Size of square
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        '''
        if not isinstance(width, int) or width <= 0:
            raise ValueError("width must be a positive integer")
        return np.ones((width, width), dtype=np.uint8)
