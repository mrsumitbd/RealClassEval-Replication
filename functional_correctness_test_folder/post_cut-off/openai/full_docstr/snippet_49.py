
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
                     Expected key: 'data' – a list or array of complex numbers.
        Returns:
            The FFT result as a list of complex numbers.
        '''
        # Extract data
        data = problem.get('data')
        if data is None:
            raise ValueError("Problem dictionary must contain 'data' key.")
        # Convert to numpy array of complex dtype
        arr = np.asarray(data, dtype=complex)
        # Compute FFT using scipy.fftpack
        result = fft(arr)
        # Return as Python list of complex numbers
        return result.tolist()

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution (list of complex numbers).
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Recompute expected result
        expected = FFTComplexScipyFFTpack.solve(problem)
        # Convert both to numpy arrays for comparison
        sol_arr = np.asarray(solution, dtype=complex)
        exp_arr = np.asarray(expected, dtype=complex)
        # Use allclose with a reasonable tolerance
        return np.allclose(sol_arr, exp_arr, atol=1e-8, rtol=1e-5)
