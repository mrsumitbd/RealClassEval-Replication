
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
                     Expected keys:
                         - 'data': list or numpy array of complex numbers
                         - optional 'n': int, length of FFT
                         - optional 'axis': int, axis along which to compute FFT
        Returns:
            The solution as a list of complex numbers
        '''
        data = problem.get('data')
        if data is None:
            raise ValueError("Problem dictionary must contain 'data' key.")
        # Convert to numpy array if not already
        arr = np.asarray(data, dtype=complex)
        n = problem.get('n', None)
        axis = problem.get('axis', None)
        # Compute FFT
        if n is not None and axis is not None:
            result = fft(arr, n=n, axis=axis)
        elif n is not None:
            result = fft(arr, n=n)
        elif axis is not None:
            result = fft(arr, axis=axis)
        else:
            result = fft(arr)
        # Return as list of complex numbers
        return result.tolist()

    @staticmethod
    def is_solution(problem, solution):
        '''
        Verify that the solution matches the expected result.
        Args:
            problem: Dictionary containing problem data and expected result
            solution: The solution returned by solve (list of complex numbers)
        Returns:
            True if solution matches expected within tolerance, False otherwise
        '''
        expected = problem.get('expected')
        if expected is None:
            # If no expected provided, cannot verify
            return False
        # Convert both to numpy arrays
        sol_arr = np.asarray(solution, dtype=complex)
        exp_arr = np.asarray(expected, dtype=complex)
        # Use allclose with a reasonable tolerance
        return np.allclose(sol_arr, exp_arr, atol=1e-6, rtol=1e-6)
