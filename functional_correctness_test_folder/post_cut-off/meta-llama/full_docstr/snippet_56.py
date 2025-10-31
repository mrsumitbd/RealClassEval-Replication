
import numpy as np
from scipy.fftpack import fft, ifft


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
        input_array = np.array(problem['input_array'], dtype=np.complex128)
        fft_result = fft(input_array)
        return {'fft_result': fft_result.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_array = np.array(problem['input_array'], dtype=np.complex128)
        expected_fft_result = fft(input_array)
        provided_fft_result = np.array(
            solution['fft_result'], dtype=np.complex128)
        return np.allclose(expected_fft_result, provided_fft_result)
