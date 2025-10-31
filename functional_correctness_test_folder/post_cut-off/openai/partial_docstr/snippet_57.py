
import numpy as np


class FFTConvolution:
    def __init__(self):
        pass

    def solve(self, problem):
        """
        Solve the fft_convolution problem.

        Parameters
        ----------
        problem : dict
            Dictionary containing problem data specific to fft_convolution.
            Expected keys:
                - 'a': list or array-like of numbers (first sequence)
                - 'b': list or array-like of numbers (second sequence)

        Returns
        -------
        list
            The convolution of sequences a and b.
        """
        a = np.asarray(problem['a'], dtype=np.complex128)
        b = np.asarray(problem['b'], dtype=np.complex128)

        n = len(a) + len(b) - 1
        # Use next power of two for efficient FFT (optional)
        fft_len = 1 << (n - 1).bit_length()

        A = np.fft.fft(a, fft_len)
        B = np.fft.fft(b, fft_len)
        C = A * B
        conv = np.fft.ifft(C)[:n]

        # If input sequences are real integers, round to nearest integer
        if np.isrealobj(a) and np.isrealobj(b):
            conv = np.rint(conv.real).astype(int)
        else:
            conv = conv.real

        return conv.tolist()

    def is_solution(self, problem, solution):
        """
        Verify that the provided solution is correct.

        Parameters
        ----------
        problem : dict
            Problem dictionary as described in `solve`.
        solution : list or array-like
            Candidate solution to verify.

        Returns
        -------
        bool
            True if the solution matches the expected convolution within tolerance.
        """
        expected = self.solve(problem)
        # Convert both to numpy arrays for comparison
        sol_arr = np.asarray(solution, dtype=np.float64)
        exp_arr = np.asarray(expected, dtype=np.float64)

        # Use a tolerance for floating point comparisons
        return np.allclose(sol_arr, exp_arr, atol=1e-6, rtol=1e-6)
