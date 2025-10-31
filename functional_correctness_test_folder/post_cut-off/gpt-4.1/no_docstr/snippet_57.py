
import numpy as np


class FFTConvolution:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        problem: tuple (a, b)
        a, b: lists or 1D numpy arrays of real or complex numbers
        Returns: list, the linear convolution of a and b using FFT
        """
        a, b = problem
        a = np.asarray(a)
        b = np.asarray(b)
        n = len(a) + len(b) - 1
        N = 1 << (n - 1).bit_length()  # Next power of 2
        A = np.fft.fft(a, N)
        B = np.fft.fft(b, N)
        C = A * B
        c = np.fft.ifft(C)
        # If input is real, output should be real
        if np.isrealobj(a) and np.isrealobj(b):
            c = np.real(c)
        return c[:n].tolist()

    def is_solution(self, problem, solution):
        """
        Checks if solution is the correct linear convolution of a and b.
        """
        expected = self.solve(problem)
        # Allow for small floating point errors
        return np.allclose(expected, solution, rtol=1e-7, atol=1e-8)
