
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
        input_matrix = np.array(problem['input'])
        kernel = np.array(problem['kernel'])

        input_height, input_width = input_matrix.shape
        kernel_height, kernel_width = kernel.shape

        output_height = input_height + kernel_height - 1
        output_width = input_width + kernel_width - 1

        output = np.zeros((output_height, output_width))

        for i in range(output_height):
            for j in range(output_width):
                for m in range(kernel_height):
                    for n in range(kernel_width):
                        input_i = i - m
                        input_j = j - n
                        if 0 <= input_i < input_height and 0 <= input_j < input_width:
                            output[i, j] += input_matrix[input_i,
                                                         input_j] * kernel[m, n]

        return output.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            computed_solution = self.solve(problem)
            return np.allclose(np.array(computed_solution), np.array(solution))
        except:
            return False
