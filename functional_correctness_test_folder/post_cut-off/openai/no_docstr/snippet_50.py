
import numpy as np


class FFTConvolution:
    def __init__(self):
        pass

    def solve(self, problem):
        """
        Compute the convolution of two integer sequences using FFT.

        Parameters
        ----------
        problem : dict
            Must contain keys 'a' and 'b', each mapping to a list of integers.

        Returns
        -------
        list[int]
            The convolution of the two sequences.
        """
        a = problem.get('a', [])
        b = problem.get('b', [])

        # Convert to numpy arrays of type float for FFT
        a_np = np.array(a, dtype=np.float64)
        b_np = np.array(b, dtype=np.float64)

        # Length of result
        n = len(a) + len(b) - 1
        # Next power of two for efficient FFT
        m = 1 << (n - 1).bit_length()

        # Zero-pad to length m
        a_pad = np.zeros(m, dtype=np.float64)
        b_pad = np.zeros(m, dtype=np.float64)
        a_pad[:len(a)] = a_np
        b_pad[:len(b)] = b_np

        # FFT, pointwise multiplication, inverse FFT
        fft_a = np.fft.fft(a_pad)
        fft_b = np.fft.fft(b_pad)
        fft_prod = fft_a * fft_b
        conv = np.fft.ifft(fft_prod)

        # Round to nearest integer and truncate to length n
        conv_real = np.rint(np.real(conv)).astype(int)
        return conv_real[:n].tolist()

    def is_solution(self, problem, solution):
        """
        Verify that the provided solution matches the expected convolution.

        Parameters
        ----------
        problem : dict
            Must contain keys 'a', 'b', and optionally 'expected'.
        solution : list[int]
            The convolution result to verify.

        Returns
        -------
        bool
            True if the solution matches the expected result or if no expected
            result is provided; False otherwise.
        """
        expected = problem.get('expected')
        if expected is None:
            # No expected value provided; assume solution is correct
            return True
        # Ensure both lists are of the same length
        if len(solution) != len(expected):
            return False
        # Compare element-wise
        return all(s == e for s, e in zip(solution, expected))
