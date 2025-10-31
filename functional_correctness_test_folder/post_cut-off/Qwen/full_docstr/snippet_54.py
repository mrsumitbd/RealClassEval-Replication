
import numpy as np


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
        Returns:
            The solution in the format expected by the task
        '''
        image = problem['image']
        kernel = problem['kernel']
        return self._convolve2d_full(image, kernel)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        image = problem['image']
        kernel = problem['kernel']
        expected_solution = self._convolve2d_full(image, kernel)
        return np.array_equal(solution, expected_solution)

    def _convolve2d_full(self, image, kernel):
        image_height, image_width = image.shape
        kernel_height, kernel_width = kernel.shape
        output_height = image_height + kernel_height - 1
        output_width = image_width + kernel_width - 1
        output = np.zeros((output_height, output_width))

        for i in range(output_height):
            for j in range(output_width):
                i_start = max(0, i - kernel_height + 1)
                i_end = min(image_height, i + 1)
                j_start = max(0, j - kernel_width + 1)
                j_end = min(image_width, j + 1)
                kernel_i_start = max(0, kernel_height - 1 - i)
                kernel_i_end = kernel_height - (i_end - i_start)
                kernel_j_start = max(0, kernel_width - 1 - j)
                kernel_j_end = kernel_width - (j_end - j_start)
                output[i, j] = np.sum(image[i_start:i_end, j_start:j_end] *
                                      kernel[kernel_i_start:kernel_i_end, kernel_j_start:kernel_j_end])
        return output
