
import numpy as np
from scipy.fftpack import fft, ifft


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
        data = problem.get('data', np.array([]))
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        fft_result = fft(data)
        return fft_result

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        data = problem.get('data', np.array([]))
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        if not isinstance(solution, np.ndarray):
            raise ValueError("Solution must be a numpy array.")
        ifft_result = ifft(solution)
        return np.allclose(ifft_result, data, atol=1e-6)
