
import numpy as np
from scipy import fftpack


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        # No special initialization required
        pass

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
                     Expected keys:
                         - 'data': array-like of complex numbers
        Returns:
            The FFT of the input data as a NumPy array of complex numbers.
        '''
        if not isinstance(problem, dict):
            raise TypeError("Problem must be a dictionary.")
        if 'data' not in problem:
            raise KeyError("Problem dictionary must contain 'data' key.")
        data = np.asarray(problem['data'], dtype=complex)
        # Compute the FFT using scipy.fftpack
        result = fftpack.fft(data)
        return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution (array-like of complex numbers).
        Returns:
            True if the solution matches the expected FFT within tolerance, False otherwise.
        '''
        # Recompute the expected solution
        expected = self.solve(problem)
        # Convert provided solution to NumPy array
        sol_arr = np.asarray(solution, dtype=complex)
        # Use allclose with a reasonable tolerance
        return np.allclose(sol_arr, expected, atol=1e-6, rtol=1e-6)
