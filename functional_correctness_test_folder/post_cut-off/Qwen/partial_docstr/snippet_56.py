
import numpy as np
from scipy.fft import fft, ifft


class FFTComplexScipyFFTpack:

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
        data = problem.get('data', np.array([]))
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        return fft(data)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        original_data = problem.get('data', np.array([]))
        if not isinstance(original_data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        reconstructed_data = ifft(solution)
        return np.allclose(original_data, reconstructed_data)
