import cv2
import numpy as np

class MorphologicalStructFactory:
    """
    Factory methods for generating morphological structuring elements
    """

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        """
        :param radius: Radius of disk
        :return: The structuring element where elements of the neighborhood are 1 and 0 otherwise.
        """
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (radius, radius))

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        """
        :param width: Width of rectangle
        :param height: Height of rectangle
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        """
        return cv2.getStructuringElement(cv2.MORPH_RECT, (height, width))

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        """
        :param width: Size of square
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        """
        return cv2.getStructuringElement(cv2.MORPH_RECT, (width, width))