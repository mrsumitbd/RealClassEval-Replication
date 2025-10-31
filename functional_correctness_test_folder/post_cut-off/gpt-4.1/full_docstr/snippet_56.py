
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
        # Expecting problem['input'] to be a list of complex numbers
        x = np.array(problem['input'], dtype=np.complex128)
        result = fft(x)
        return result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        x = np.array(problem['input'], dtype=np.complex128)
        expected = fft(x)
        sol = np.array(solution, dtype=np.complex128)
        if sol.shape != expected.shape:
            return False
        return np.allclose(sol, expected, rtol=1e-7, atol=1e-8)
