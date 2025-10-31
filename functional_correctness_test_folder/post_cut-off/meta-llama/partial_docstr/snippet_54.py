
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
        input_matrix = np.array(problem['input_matrix'])
        kernel = np.array(problem['kernel'])

        input_height, input_width = input_matrix.shape
        kernel_height, kernel_width = kernel.shape

        output_height = input_height + kernel_height - 1
        output_width = input_width + kernel_width - 1

        output_matrix = np.zeros((output_height, output_width))

        for i in range(output_height):
            for j in range(output_width):
                for k in range(kernel_height):
                    for l in range(kernel_width):
                        input_i = i - k
                        input_j = j - l
                        if 0 <= input_i < input_height and 0 <= input_j < input_width:
                            output_matrix[i, j] += input_matrix[input_i, input_j] * \
                                kernel[kernel_height - 1 -
                                       k, kernel_width - 1 - l]

        return output_matrix.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_matrix = np.array(problem['input_matrix'])
        kernel = np.array(problem['kernel'])
        expected_output = np.array(solution)

        input_height, input_width = input_matrix.shape
        kernel_height, kernel_width = kernel.shape
        output_height, output_width = expected_output.shape

        if output_height != input_height + kernel_height - 1 or output_width != input_width + kernel_width - 1:
            return False

        output_matrix = np.zeros((output_height, output_width))

        for i in range(output_height):
            for j in range(output_width):
                for k in range(kernel_height):
                    for l in range(kernel_width):
                        input_i = i - k
                        input_j = j - l
                        if 0 <= input_i < input_height and 0 <= input_j < input_width:
                            output_matrix[i, j] += input_matrix[input_i, input_j] * \
                                kernel[kernel_height - 1 -
                                       k, kernel_width - 1 - l]

        return np.allclose(output_matrix, expected_output)
