
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        '''
        :param radius: Radius of disk
        :return: The structuring element where elements of the neighborhood are 1 and 0 otherwise.
        '''
        diameter = 2 * radius + 1
        struct = np.zeros((diameter, diameter))
        for i in range(diameter):
            for j in range(diameter):
                if (i - radius) ** 2 + (j - radius) ** 2 <= radius ** 2:
                    struct[i, j] = 1
        return struct

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        '''
        :param width: Width of rectangle
        :param height: Height of rectangle
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        '''
        return np.ones((height, width))

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        '''
        :param width: Size of square
        :return: A structuring element consisting only of ones, i.e. every pixel belongs to the neighborhood.
        '''
        return np.ones((width, width))


# Example usage:
if __name__ == "__main__":
    print(MorphologicalStructFactory.get_disk(2))
    print(MorphologicalStructFactory.get_rectangle(3, 4))
    print(MorphologicalStructFactory.get_square(3))
