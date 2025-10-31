
import numpy as np


class FFTConvolution:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a = np.array(problem['a'])
        b = np.array(problem['b'])
        n = len(a)
        m = len(b)
        size = n + m - 1
        # Next power of 2 for efficient FFT
        fft_size = 1 << (size - 1).bit_length()
        fa = np.fft.fft(a, fft_size)
        fb = np.fft.fft(b, fft_size)
        fc = fa * fb
        c = np.fft.ifft(fc)
        # Only take the real part and round to avoid floating point errors
        result = np.rint(np.real(c[:size])).astype(int)
        return result.tolist()

    def is_solution(self, problem, solution):
        a = problem['a']
        b = problem['b']
        expected = []
        n = len(a)
        m = len(b)
        for k in range(n + m - 1):
            s = 0
            for i in range(n):
                j = k - i
                if 0 <= j < m:
                    s += a[i] * b[j]
            expected.append(s)
        return expected == solution
