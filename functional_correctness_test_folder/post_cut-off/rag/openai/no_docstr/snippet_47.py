
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
        if not isinstance(problem, tuple) or len(problem) != 2:
            raise ValueError("Problem must be a tuple (a, b) of 2D arrays.")
        a, b = problem
        a = np.asarray(a)
        b = np.asarray(b)
        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("Both inputs must be 2‑D arrays.")
        # fftconvolve with mode='full' gives the full convolution
        return fftconvolve(a, b, mode='full')

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
            expected = self.solve(problem)
        except Exception:
            return False
        # Use allclose for floating point arrays, otherwise array_equal
        if isinstance(expected, np.ndarray) and isinstance(solution, np.ndarray):
            return np.allclose(expected, solution, atol=1e-8, rtol=1e-5)
        return expected == solution
