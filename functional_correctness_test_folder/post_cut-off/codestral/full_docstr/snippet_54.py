
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
        input_array = problem['input_array']
        kernel = problem['kernel']
        solution = np.zeros(
            (input_array.shape[0] + kernel.shape[0] - 1, input_array.shape[1] + kernel.shape[1] - 1))
        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):
                solution[i:i+kernel.shape[0], j:j+kernel.shape[1]
                         ] += input_array[i, j] * kernel
        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_array = problem['input_array']
        kernel = problem['kernel']
        expected_solution = np.zeros(
            (input_array.shape[0] + kernel.shape[0] - 1, input_array.shape[1] + kernel.shape[1] - 1))
        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):
                expected_solution[i:i+kernel.shape[0], j:j +
                                  kernel.shape[1]] += input_array[i, j] * kernel
        return np.array_equal(solution, expected_solution)
