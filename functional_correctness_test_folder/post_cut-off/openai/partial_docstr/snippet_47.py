
import numpy as np
from scipy.signal import fftconvolve


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
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
        # Perform full convolution
        result = fftconvolve(a, b, mode='full')
        return result

    def is_solution(self, problem, solution):
        '''
        Verify that the provided solution matches the expected full convolution
        with fill boundary. Uses numpy's allclose for comparison.
        Args:
            problem: A tuple (a, b) of 2D arrays.
            solution: The candidate solution array.
        Returns:
            True if solution is close to the expected result, False otherwise.
        '''
        expected = self.solve(problem)
        return np.allclose(solution, expected, atol=1e-8, rtol=1e-5)
