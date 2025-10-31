
import numpy as np
from scipy.fftpack import fft


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def solve(problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        input_data = problem.get('input_data', [])
        solution = fft(input_data)
        return solution

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is correct for the given problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
            solution: The solution to be checked
        Returns:
            Boolean indicating if the solution is correct
        '''
        input_data = problem.get('input_data', [])
        expected_solution = fft(input_data)
        return np.allclose(solution, expected_solution)
