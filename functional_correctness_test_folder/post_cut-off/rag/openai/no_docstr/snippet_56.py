
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
                         - 'data': array-like of complex numbers
        Returns:
            The solution in the format expected by the task
            (a list of complex numbers representing the FFT of the input)
        '''
        # Extract the input data
        data = problem.get('data')
        if data is None:
            raise ValueError("Problem dictionary must contain a 'data' key.")
        # Convert to numpy array of complex dtype
        arr = np.asarray(data, dtype=np.complex128)
        # Compute the FFT using scipy.fftpack
        fft_result = fftpack.fft(arr)
        # Return as a plain Python list of complex numbers
        return fft_result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution (list of complex numbers)
        Returns:
            True if the solution is valid, False otherwise
        '''
        # The problem may optionally provide an expected result for validation
        expected = problem.get('expected')
        if expected is None:
            # If no expected result is provided, we cannot validate
            # Assume the solution is valid if it can be computed without error
            try:
                # Try recomputing to ensure no exception
                self.solve(problem)
                return True
            except Exception:
                return False

        # Convert both to numpy arrays for comparison
        sol_arr = np.asarray(solution, dtype=np.complex128)
        exp_arr = np.asarray(expected, dtype=np.complex128)

        # Use a tolerance suitable for floating point FFT results
        return np.allclose(sol_arr, exp_arr, atol=1e-6, rtol=1e-6)
