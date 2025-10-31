import numpy as np
from scipy.signal import convolve2d


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
        input_matrix = np.array(problem['input'], dtype=float)
        kernel = np.array(problem['kernel'], dtype=float)
        result = convolve2d(input_matrix, kernel, mode='full',
                            boundary='fill', fillvalue=0)
        return result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        expected = self.solve(problem)
        # Allow for floating point tolerance
        arr1 = np.array(expected)
        arr2 = np.array(solution)
        if arr1.shape != arr2.shape:
            return False
        return np.allclose(arr1, arr2, atol=1e-8)
