
import numpy as np
from scipy.signal import fftconvolve


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Compute the 2D convolution of arrays a and b using "full" mode and "fill" boundary.
        Uses scipy.signal.fftconvolve for efficiency, which implicitly handles "fill" boundary.
        Args:
            problem: A tuple (a, b) of 2D arrays.
        Returns:
            A 2D array containing the convolution result.
        '''
        a, b = problem
        # Ensure inputs are numpy arrays
        a = np.asarray(a)
        b = np.asarray(b)
        # Perform full convolution with zero padding (fill)
        result = fftconvolve(a, b, mode='full')
        return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        a, b = problem
        expected = self.solve(problem)
        # Use allclose for floating point arrays, otherwise array_equal
        if np.issubdtype(solution.dtype, np.floating) or np.issubdtype(expected.dtype, np.floating):
            return np.allclose(solution, expected, atol=1e-8, rtol=1e-5)
        else:
            return np.array_equal(solution, expected)
