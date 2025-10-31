
import numpy as np


class FFTConvolution:

    def __init__(self):
        pass

    def solve(self, problem):
        # problem: tuple (a, b), both are lists or 1D numpy arrays
        a, b = problem
        a = np.asarray(a, dtype=np.float64)
        b = np.asarray(b, dtype=np.float64)
        n = len(a)
        m = len(b)
        size = n + m - 1
        N = 1 << (size - 1).bit_length()  # next power of 2
        A = np.fft.fft(a, N)
        B = np.fft.fft(b, N)
        C = A * B
        c = np.fft.ifft(C)
        c = np.real(c[:size])
        # Round to avoid floating point errors
        c = np.round(c, decimals=10)
        return c.tolist()

    def is_solution(self, problem, solution):
        # Check if solution is the convolution of a and b
        expected = self.solve(problem)
        # Allow small floating point errors
        if len(expected) != len(solution):
            return False
        for x, y in zip(expected, solution):
            if abs(x - y) > 1e-8:
                return False
        return True
