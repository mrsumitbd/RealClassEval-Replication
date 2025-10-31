
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
                Expected keys:
                    - 'input': list or np.ndarray of complex numbers (the signal)
                    - 'inverse': bool (if True, compute inverse FFT; else, forward FFT)
        Returns:
            The solution in the format expected by the task: list of complex numbers
        '''
        x = problem.get('input', [])
        inverse = problem.get('inverse', False)
        arr = np.asarray(x, dtype=np.complex128)
        if inverse:
            result = ifft(arr)
        else:
            result = fft(arr)
        return result.tolist()

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
        x = problem.get('input', [])
        inverse = problem.get('inverse', False)
        arr = np.asarray(x, dtype=np.complex128)
        if inverse:
            expected = ifft(arr)
        else:
            expected = fft(arr)
        sol = np.asarray(solution, dtype=np.complex128)
        if sol.shape != expected.shape:
            return False
        return np.allclose(sol, expected, rtol=1e-7, atol=1e-8)
