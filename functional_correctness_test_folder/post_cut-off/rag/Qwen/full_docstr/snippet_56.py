
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
                "Problem must contain 'data' key with the input array.")
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        if data.dtype != np.complex128:
            raise ValueError("Data must be of type np.complex128.")

        fft_result = fftpack.fft2(data)
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
            return False
        if not isinstance(data, np.ndarray):
            return False
        if data.dtype != np.complex128:
            return False
        if not isinstance(solution, np.ndarray):
            return False
        if solution.shape != data.shape:
            return False
        if solution.dtype != np.complex128:
            return False

        # Reconstruct the data from the solution and compare with the original data
        ifft_result = fftpack.ifft2(solution)
        return np.allclose(ifft_result, data)
