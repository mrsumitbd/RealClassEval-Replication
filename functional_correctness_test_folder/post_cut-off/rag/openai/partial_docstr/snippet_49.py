
import numpy as np
from scipy import fftpack


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
                     - 'data': array-like of complex numbers
                     - optional 'axis': int, axis along which to compute the FFT (default 0)
                     - optional 'norm': str, normalization mode ('forward', 'backward', 'ortho') (default None)
        Returns:
            The solution as a numpy array containing the FFT result.
        '''
        # Extract data and parameters
        data = problem.get('data')
        if data is None:
            raise ValueError("Problem dictionary must contain 'data' key.")
        data = np.asarray(data, dtype=complex)

        axis = problem.get('axis', 0)
        norm = problem.get('norm', None)

        # Compute FFT using scipy.fftpack
        result = fftpack.fft(data, axis=axis, norm=norm)
        return result

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution (numpy array or array-like).
        Returns:
            True if the solution is valid (matches the FFT computed by scipy.fftpack),
            False otherwise.
        '''
        # Recompute expected solution
        try:
            expected = FFTComplexScipyFFTpack.solve(problem)
        except Exception:
            return False

        # Convert solution to numpy array
        try:
            sol_arr = np.asarray(solution, dtype=complex)
        except Exception:
            return False

        # Compare shapes
        if expected.shape != sol_arr.shape:
            return False

        # Compare values with tolerance
        return np.allclose(expected, sol_arr, atol=1e-6, rtol=1e-6)
