
import numpy as np
from scipy.fftpack import fft


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
        input_data = problem.get('input_data', [])
        if not isinstance(input_data, (list, np.ndarray)):
            raise ValueError("Input data must be a list or numpy array")

        input_array = np.array(input_data, dtype=np.complex128)
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
        if not isinstance(solution, dict) or 'fft_result' not in solution:
            return False

        input_data = problem.get('input_data', [])
        expected_fft = fft(np.array(input_data, dtype=np.complex128))
        provided_fft = np.array(solution['fft_result'], dtype=np.complex128)

        if len(expected_fft) != len(provided_fft):
            return False

        return np.allclose(expected_fft, provided_fft, rtol=1e-5, atol=1e-8)
