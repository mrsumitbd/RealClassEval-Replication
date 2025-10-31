
import numpy as np
from scipy.fftpack import fft


class FFTComplexScipyFFTpack:

    @staticmethod
    def solve(problem):
        """
        Compute the FFT of a list of complex numbers using scipy.fftpack.

        Parameters
        ----------
        problem : dict
            Must contain a key 'data' with a list or array of complex numbers.

        Returns
        -------
        list
            The FFT result as a list of complex numbers.
        """
        if not isinstance(problem, dict):
            raise TypeError("Problem must be a dictionary.")
        if 'data' not in problem:
            raise KeyError("Problem dictionary must contain 'data' key.")
        data = problem['data']
        # Ensure data is a NumPy array of complex dtype
        arr = np.asarray(data, dtype=complex)
        # Compute FFT
        result = fft(arr)
        # Return as plain Python list of complex numbers
        return result.tolist()

    @staticmethod
    def is_solution(problem, solution):
        """
        Verify that the solution matches the expected FFT result.

        Parameters
        ----------
        problem : dict
            Must contain a key 'expected' with the expected FFT result.
        solution : list
            The FFT result produced by `solve`.

        Returns
        -------
        bool
            True if the solution matches the expected result within tolerance.
        """
        if not isinstance(problem, dict):
            raise TypeError("Problem must be a dictionary.")
        if 'expected' not in problem:
            raise KeyError("Problem dictionary must contain 'expected' key.")
        expected = problem['expected']
        # Convert both to NumPy arrays for comparison
        sol_arr = np.asarray(solution, dtype=complex)
        exp_arr = np.asarray(expected, dtype=complex)
        # Use allclose with a reasonable tolerance
        return np.allclose(sol_arr, exp_arr, atol=1e-6, rtol=1e-6)
