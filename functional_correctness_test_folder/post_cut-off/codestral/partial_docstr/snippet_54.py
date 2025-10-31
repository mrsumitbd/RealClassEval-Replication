
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
        Solve the 2D convolution problem using full mode.
        Args:
            problem: A dictionary containing 'input' and 'kernel' keys
        Returns:
            The result of the 2D convolution in full mode
        '''
        input_array = problem['input']
        kernel = problem['kernel']
        return np.convolve(input_array, kernel, mode='full')

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_array = problem['input']
        kernel = problem['kernel']
        expected_solution = np.convolve(input_array, kernel, mode='full')
        return np.array_equal(solution, expected_solution)
