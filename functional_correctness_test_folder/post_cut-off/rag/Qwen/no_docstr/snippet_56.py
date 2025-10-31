
import numpy as np
from scipy import fftpack


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
        data = problem.get('data', None)
        if data is None:
            raise ValueError(
                "Problem dictionary must contain 'data' key with complex array.")
        if not isinstance(data, np.ndarray) or not np.iscomplexobj(data):
            raise ValueError("Data must be a numpy array of complex numbers.")

        # Perform FFT using scipy's fftpack
        fft_result = fftpack.fft(data)
        return fft_result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        data = problem.get('data', None)
        if data is None:
            raise ValueError(
                "Problem dictionary must contain 'data' key with complex array.")
        if not isinstance(data, np.ndarray) or not np.iscomplexobj(data):
            raise ValueError("Data must be a numpy array of complex numbers.")
        if not isinstance(solution, np.ndarray) or not np.iscomplexobj(solution):
            raise ValueError(
                "Solution must be a numpy array of complex numbers.")
        if solution.shape != data.shape:
            return False

        # Reconstruct the original data from the solution (inverse FFT)
        reconstructed_data = fftpack.ifft(solution)

        # Check if the reconstructed data matches the original data within a tolerance
        return np.allclose(data, reconstructed_data, atol=1e-6)
