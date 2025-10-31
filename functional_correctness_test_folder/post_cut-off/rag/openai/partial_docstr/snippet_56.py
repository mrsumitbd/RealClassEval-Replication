
import numpy as np
from scipy import fftpack


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
                     Expected keys:
                         - 'data': iterable of complex numbers (list, tuple, np.ndarray)
                         - optionally 'expected': iterable of complex numbers for validation
        Returns:
            The solution in the format expected by the task: a list of complex numbers
        '''
        # Extract the input data
        data = problem.get('data')
        if data is None:
            raise ValueError("Problem dictionary must contain 'data' key")

        # Convert to a NumPy array of complex dtype
        arr = np.asarray(data, dtype=np.complex128)

        # Compute the FFT using scipy.fftpack
        fft_result = fftpack.fft(arr)

        # Return as a plain Python list of complex numbers
        return fft_result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (list of complex numbers)
        Returns:
            True if the solution is valid, False otherwise
        '''
        # If the problem provides an expected result, compare against it
        expected = problem.get('expected')
        if expected is not None:
            # Convert both to NumPy arrays for comparison
            sol_arr = np.asarray(solution, dtype=np.complex128)
            exp_arr = np.asarray(expected, dtype=np.complex128)
            return np.allclose(sol_arr, exp_arr, atol=1e-6, rtol=1e-6)

        # Otherwise, recompute the FFT and compare
        try:
            recomputed = self.solve(problem)
        except Exception:
            return False

        sol_arr = np.asarray(solution, dtype=np.complex128)
        recomputed_arr = np.asarray(recomputed, dtype=np.complex128)
        return np.allclose(sol_arr, recomputed_arr, atol=1e-6, rtol=1e-6)
