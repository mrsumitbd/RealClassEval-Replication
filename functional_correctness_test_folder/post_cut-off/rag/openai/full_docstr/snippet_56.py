
import numpy as np
from scipy import fftpack


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        # No special initialization required for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        # Expect the problem to contain a key 'data' with a list/array of complex numbers
        if not isinstance(problem, dict):
            raise ValueError("Problem must be a dictionary.")
        if 'data' not in problem:
            raise KeyError("Problem dictionary must contain 'data' key.")
        data = problem['data']

        # Convert to numpy array of complex dtype
        arr = np.asarray(data, dtype=np.complex128)

        # Compute the FFT using scipy.fftpack
        fft_result = fftpack.fft(arr)

        # Return as a list of complex numbers
        return fft_result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Recompute the expected solution
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Ensure solution is a list/array of complex numbers
        try:
            sol_arr = np.asarray(solution, dtype=np.complex128)
        except Exception:
            return False

        # Compare with a tolerance
        return np.allclose(sol_arr, expected, atol=1e-6, rtol=1e-6)
