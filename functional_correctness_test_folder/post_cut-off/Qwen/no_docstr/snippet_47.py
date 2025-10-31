
import numpy as np


class Convolve2DFullFill:

    def __init__(self):
        pass

    def solve(self, problem):
        image, kernel = problem
        return self._convolve2d_full(image, kernel)

    def is_solution(self, problem, solution):
        image, kernel = problem
        expected_solution = self._convolve2d_full(image, kernel)
        return np.array_equal(solution, expected_solution)

    def _convolve2d_full(self, image, kernel):
        image_h, image_w = image.shape
        kernel_h, kernel_w = kernel.shape
        output_h = image_h + kernel_h - 1
        output_w = image_w + kernel_w - 1
        output = np.zeros((output_h, output_w))

        for i in range(output_h):
            for j in range(output_w):
                i_start = max(0, i - kernel_h + 1)
                i_end = min(image_h, i + 1)
                j_start = max(0, j - kernel_w + 1)
                j_end = min(image_w, j + 1)
                kernel_i_start = max(0, kernel_h - 1 - i)
                kernel_i_end = kernel_h - (i_end - i_start)
                kernel_j_start = max(0, kernel_w - 1 - j)
                kernel_j_end = kernel_w - (j_end - j_start)
                output[i, j] = np.sum(image[i_start:i_end, j_start:j_end] *
                                      kernel[kernel_i_start:kernel_i_end, kernel_j_start:kernel_j_end])

        return output
