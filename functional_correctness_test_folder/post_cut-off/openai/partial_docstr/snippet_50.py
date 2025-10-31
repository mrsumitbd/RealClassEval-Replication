
import numpy as np


class FFTConvolution:
    def __init__(self):
        '''Initialize the FFTConvolution.'''
        pass

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
                     Expected keys: 'a' and 'b', each a list or array of numbers.
        Returns:
            The convolution of a and b as a list of numbers.
        '''
        a = np.asarray(problem['a'], dtype=np.float64)
        b = np.asarray(problem['b'], dtype=np.float64)

        # Length of the linear convolution result
        n = len(a) + len(b) - 1

        # Next power of two for efficient FFT
        fft_len = 1 << (n - 1).bit_length()

        # Zero‑pad sequences
        A = np.fft.fft(a, fft_len)
        B = np.fft.fft(b, fft_len)

        # Element‑wise multiplication in frequency domain
        C = A * B

        # Inverse FFT to get back to time domain
        conv = np.fft.ifft(C).real

        # Truncate to the exact length and round small imaginary parts
        conv = conv[:n]

        # If the input sequences were integers, round to nearest integer
        if np.all(np.mod(a, 1) == 0) and np.all(np.mod(b, 1) == 0):
            conv = np.rint(conv).astype(int)

        return conv.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution (list of numbers).
        Returns:
            True if the solution matches the expected convolution, False otherwise.
        '''
        expected = self.solve(problem)

        # Convert both to numpy arrays for comparison
        sol_arr = np.asarray(solution, dtype=np.float64)
        exp_arr = np.asarray(expected, dtype=np.float64)

        # If both are integer sequences, compare exactly
        if np.all(np.mod(sol_arr, 1) == 0) and np.all(np.mod(exp_arr, 1) == 0):
            return np.array_equal(sol_arr.astype(int), exp_arr.astype(int))

        # Otherwise allow a small tolerance for floating point errors
        return np.allclose(sol_arr, exp_arr, atol=1e-6, rtol=1e-6)
