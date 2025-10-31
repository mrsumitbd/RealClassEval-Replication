
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
                     Expected keys: 'a' and 'b', each a list or 1‑D array of numbers.
        Returns:
            The solution as a list of floats representing the linear convolution of a and b.
        '''
        # Extract input sequences
        a = np.asarray(problem.get('a', []), dtype=np.float64)
        b = np.asarray(problem.get('b', []), dtype=np.float64)

        if a.ndim != 1 or b.ndim != 1:
            raise ValueError("Inputs 'a' and 'b' must be 1‑D sequences.")

        # Length of the linear convolution
        n = a.size + b.size - 1

        # Pad to next power of two for efficient FFT
        m = 1 << (n - 1).bit_length()

        # Compute FFTs
        fa = np.fft.rfft(a, n=m)
        fb = np.fft.rfft(b, n=m)

        # Element‑wise multiplication and inverse FFT
        conv = np.fft.irfft(fa * fb, n=m)

        # Truncate to the true convolution length
        conv = conv[:n]

        # Return as a plain Python list
        return conv.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution (list or array).
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Compute expected solution
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Convert solution to numpy array for comparison
        try:
            sol_arr = np.asarray(solution, dtype=np.float64)
        except Exception:
            return False

        # Ensure shapes match
        if sol_arr.shape != np.asarray(expected).shape:
            return False

        # Compare with tolerance
        return np.allclose(sol_arr, expected, atol=1e-6, rtol=1e-6)
