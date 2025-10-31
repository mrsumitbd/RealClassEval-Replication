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
        # problem['input'] is expected to be a list of complex numbers or numbers
        x = np.array(problem['input'], dtype=np.complex128)
        result = fft(x)
        # Return as list of complex numbers
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
        # Reconstruct the input by inverse FFT and compare to original
        x = np.array(problem['input'], dtype=np.complex128)
        y = np.array(solution, dtype=np.complex128)
        x_rec = ifft(y)
        # Allow for small numerical errors
        return np.allclose(x, x_rec, atol=1e-8)
