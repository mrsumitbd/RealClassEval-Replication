
import numpy as np


class MorphologicalStructFactory:

    @staticmethod
    def get_disk(radius: int) -> np.ndarray:
        diameter = 2 * radius + 1
        struct = np.zeros((diameter, diameter), dtype=np.uint8)
        for i in range(diameter):
            for j in range(diameter):
                if (i - radius) ** 2 + (j - radius) ** 2 <= radius ** 2:
                    struct[i, j] = 1
        return struct

    @staticmethod
    def get_rectangle(width: int, height: int) -> np.ndarray:
        return np.ones((height, width), dtype=np.uint8)

    @staticmethod
    def get_square(width: int) -> np.ndarray:
        return np.ones((width, width), dtype=np.uint8)


# Example usage:
if __name__ == "__main__":
    disk = MorphologicalStructFactory.get_disk(3)
    rectangle = MorphologicalStructFactory.get_rectangle(5, 3)
    square = MorphologicalStructFactory.get_square(4)

    print("Disk:")
    print(disk)
    print("\nRectangle:")
    print(rectangle)
    print("\nSquare:")
    print(square)
