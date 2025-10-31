
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
            The solution as a list of real numbers representing the linear convolution
            of a and b.
        '''
        # Validate input
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")
        if 'a' not in problem or 'b' not in problem:
            raise KeyError("problem must contain keys 'a' and 'b'")

        a = np.asarray(problem['a'], dtype=np.float64)
        b = np.asarray(problem['b'], dtype=np.float64)

        if a.ndim != 1 or b.ndim != 1:
            raise ValueError("inputs 'a' and 'b' must be 1‑D arrays")

        # Length of the linear convolution
        n = a.size + b.size - 1

        # Use next power of two for efficient FFT (optional but common)
        fft_len = 1 << (n - 1).bit_length()

        # Compute FFTs
        A = np.fft.rfft(a, n=fft_len)
        B = np.fft.rfft(b, n=fft_len)

        # Element‑wise multiplication
        C = A * B

        # Inverse FFT to get convolution
        conv = np.fft.irfft(C, n=fft_len)

        # Truncate to the exact length
        conv = conv[:n]

        # Convert to Python list of floats
        return conv.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dict (same format as in solve)
            solution: The proposed solution (list or array of numbers)
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Compute expected solution
        expected = self.solve(problem)

        # Convert solution to array for comparison
        try:
            sol_arr = np.asarray(solution, dtype=np.float64)
        except Exception:
            return False

        if sol_arr.shape != np.asarray(expected).shape:
            return False

        # Use a tolerance for floating point comparison
        return np.allclose(sol_arr, expected, atol=1e-6, rtol=1e-6)
