
import numpy as np


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
                     Expected keys:
                         - 'a': list or 1‑D array of real numbers
                         - 'b': list or 1‑D array of real numbers
        Returns:
            The solution as a list of real numbers (rounded to nearest integer if inputs are integers)
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")

        if 'a' not in problem or 'b' not in problem:
            raise KeyError("problem must contain keys 'a' and 'b'")

        a = np.asarray(problem['a'], dtype=float)
        b = np.asarray(problem['b'], dtype=float)

        if a.ndim != 1 or b.ndim != 1:
            raise ValueError("inputs 'a' and 'b' must be 1‑D arrays")

        n = a.size + b.size - 1
        # next power of two for efficient FFT
        size = 1 << (n - 1).bit_length()

        # FFT of padded arrays
        fa = np.fft.rfft(a, n=size)
        fb = np.fft.rfft(b, n=size)

        # element‑wise multiplication
        fc = fa * fb

        # inverse FFT to get convolution
        conv = np.fft.irfft(fc, n=size)[:n]

        # If inputs were integers, round to nearest integer
        if np.all(np.mod(a, 1) == 0) and np.all(np.mod(b, 1) == 0):
            conv = np.rint(conv)

        return conv.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dict
            solution: The proposed solution (list or array)
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Convert solution to numpy array for comparison
        try:
            sol_arr = np.asarray(solution, dtype=float)
        except Exception:
            return False

        if sol_arr.shape != np.asarray(expected).shape:
            return False

        # Use a tolerance for floating point comparisons
        return np.allclose(sol_arr, expected, atol=1e-6)
