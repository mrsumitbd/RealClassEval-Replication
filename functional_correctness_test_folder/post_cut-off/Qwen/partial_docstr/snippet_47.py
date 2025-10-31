
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
        return fftconvolve(a, b, mode='full')

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is correct for the given problem.
        Args:
            problem: A tuple (a, b) of 2D arrays.
            solution: A 2D array that is the supposed convolution result.
        Returns:
            A boolean indicating if the solution is correct.
        '''
        a, b = problem
        expected_solution = fftconvolve(a, b, mode='full')
        return np.array_equal(solution, expected_solution)
