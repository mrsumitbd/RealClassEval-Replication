
import numpy as np


class FFTConvolution:

    def __init__(self):
        pass

    def solve(self, problem):
        a, b = problem
        n = len(a) + len(b) - 1
        fft_a = np.fft.fft(a, n)
        fft_b = np.fft.fft(b, n)
        fft_result = fft_a * fft_b
        result = np.fft.ifft(fft_result).real
        return result

    def is_solution(self, problem, solution):
        a, b = problem
        expected = np.convolve(a, b)
        return np.allclose(solution, expected, rtol=1e-5, atol=1e-8)
