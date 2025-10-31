
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
                     - optional 'axis': int, axis along which to compute the FFT
                     - optional 'norm': str or None, normalization mode ('forward', 'backward', 'ortho')
        Returns:
            The solution in the format expected by the task (numpy array of complex numbers)
        '''
        data = np.asarray(problem['data'])
        axis = problem.get('axis', None)
        norm = problem.get('norm', None)

        # scipy.fftpack.fft accepts axis and norm parameters
        result = fftpack.fft(data, axis=axis, norm=norm)
        return result

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
        try:
            expected = FFTComplexScipyFFTpack.solve(problem)
        except Exception:
            return False

        # Ensure solution is array-like
        try:
            sol_arr = np.asarray(solution)
        except Exception:
            return False

        # Compare shapes
        if sol_arr.shape != expected.shape:
            return False

        # Compare values with tolerance
        return np.allclose(sol_arr, expected, atol=1e-6, rtol=1e-6)
