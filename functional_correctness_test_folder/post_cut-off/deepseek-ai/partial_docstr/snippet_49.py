
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
        input_data = problem['input']
        fft_result = fft(input_data)
        return fft_result.tolist()

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the solution is correct for the given problem.
        Args:
            problem: Dictionary containing problem data
            solution: Proposed solution to verify
        Returns:
            bool: True if the solution is correct, False otherwise
        '''
        input_data = problem['input']
        expected_result = fft(input_data)
        return np.allclose(solution, expected_result)
