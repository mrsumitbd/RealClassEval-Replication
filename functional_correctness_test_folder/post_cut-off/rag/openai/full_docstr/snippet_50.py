
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
                         - 'a': list or array-like of numbers
                         - 'b': list or array-like of numbers
        Returns:
            The solution as a list of numbers (rounded to nearest integer if inputs are ints)
        '''
        a = np.asarray(problem.get('a', []), dtype=float)
        b = np.asarray(problem.get('b', []), dtype=float)

        if a.size == 0 or b.size == 0:
            return []

        # Length of convolution result
        conv_len = a.size + b.size - 1
        # Next power of two for efficient FFT
        n = 1 << (conv_len - 1).bit_length()

        # FFT of zero-padded inputs
        fft_a = np.fft.fft(a, n)
        fft_b = np.fft.fft(b, n)

        # Element-wise multiplication in frequency domain
        fft_prod = fft_a * fft_b

        # Inverse FFT to get convolution result
        conv = np.fft.ifft(fft_prod).real

        # Truncate to the exact convolution length
        conv = conv[:conv_len]

        # If inputs were integers, round to nearest integer
        if np.all(np.mod(a, 1) == 0) and np.all(np.mod(b, 1) == 0):
            conv = np.rint(conv).astype(int)

        return conv.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (list or array-like)
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Recompute expected solution
        expected = self.solve(problem)

        # Convert both to numpy arrays for comparison
        sol_arr = np.asarray(solution, dtype=float)
        exp_arr = np.asarray(expected, dtype=float)

        # Use a tolerance for floating point comparisons
        return np.allclose(sol_arr, exp_arr, atol=1e-6)
