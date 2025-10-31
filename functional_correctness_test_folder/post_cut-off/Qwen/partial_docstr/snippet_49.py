
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
        data = problem.get('data', [])
        if not isinstance(data, (list, np.ndarray)):
            raise ValueError("Data must be a list or numpy array.")
        data = np.array(data, dtype=complex)
        return fft(data)

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is correct for the given problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
            solution: The solution to be verified
        Returns:
            True if the solution is correct, False otherwise
        '''
        expected_solution = FFTComplexScipyFFTpack.solve(problem)
        return np.allclose(solution, expected_solution)
