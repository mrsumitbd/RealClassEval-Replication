
import numpy as np


class Convolve2DFullFill:

    def __init__(self):
        pass

    def solve(self, problem):
        image, kernel = problem
        if len(image.shape) != 2 or len(kernel.shape) != 2:
            raise ValueError("Image and kernel must be 2D arrays")

        image_height, image_width = image.shape
        kernel_height, kernel_width = kernel.shape

        # Calculate output dimensions
        output_height = image_height + kernel_height - 1
        output_width = image_width + kernel_width - 1

        # Pad the image with zeros
        padded_image = np.zeros((output_height, output_width))
        pad_top = kernel_height - 1
        pad_left = kernel_width - 1

        # Place the original image in the padded array
        padded_image[pad_top:pad_top + image_height,
                     pad_left:pad_left + image_width] = image

        # Initialize the output
        output = np.zeros((output_height, output_width))

        # Perform convolution
        for i in range(output_height):
            for j in range(output_width):
                for m in range(kernel_height):
                    for n in range(kernel_width):
                        if 0 <= i - m < output_height and 0 <= j - n < output_width:
                            output[i, j] += padded_image[i -
                                                         m, j - n] * kernel[m, n]

        return output

    def is_solution(self, problem, solution):
        try:
            computed_solution = self.solve(problem)
            return np.allclose(computed_solution, solution)
        except:
            return False
