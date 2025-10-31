
import numpy as np
from scipy import fftpack


class FFTComplexScipyFFTpack:
    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        # No special initialization required
        pass

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
                     Expected keys:
                         - "data": list or numpy array of complex numbers
        Returns:
            The solution as a list of complex numbers (the FFT of the input data)
        '''
        # Extract data
        data = problem.get("data")
        if data is None:
            raise ValueError("Problem dictionary must contain 'data' key.")
        # Convert to numpy array of complex dtype
        arr = np.asarray(data, dtype=complex)
        # Compute FFT using scipy.fftpack
        fft_result = fftpack.fft(arr)
        # Return as list of complex numbers
        return fft_result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (list of complex numbers)
        Returns:
            True if the solution is valid (within tolerance), False otherwise
        '''
        # Compute expected solution
        expected = self.solve(problem)
        # Convert both to numpy arrays
        sol_arr = np.asarray(solution, dtype=complex)
        exp_arr = np.asarray(expected, dtype=complex)
        # Use allclose with default tolerances
        return np.allclose(sol_arr, exp_arr, atol=1e-8, rtol=1e-5)
