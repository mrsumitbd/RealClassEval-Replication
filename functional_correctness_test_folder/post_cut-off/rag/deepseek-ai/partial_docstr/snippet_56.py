
import numpy as np
from scipy import fftpack


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        pass

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        input_data = problem['input']
        if isinstance(input_data, list):
            input_data = np.array(input_data)
        fft_result = fftpack.fft(input_data)
        return fft_result.tolist()

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
            input_data = problem['input']
            if isinstance(input_data, list):
                input_data = np.array(input_data)
            expected_result = fftpack.fft(input_data)
            return np.allclose(solution, expected_result)
        except:
            return False
