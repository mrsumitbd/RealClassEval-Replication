
import numpy as np


class FFTConvolution:

    def __init__(self):
        pass

    def solve(self, problem):
        signal, kernel = problem
        n = len(signal)
        m = len(kernel)
        size = n + m - 1
        fft_signal = np.fft.fft(signal, size)
        fft_kernel = np.fft.fft(kernel, size)
        convolved = np.fft.ifft(fft_signal * fft_kernel).real
        return convolved

    def is_solution(self, problem, solution):
        signal, kernel = problem
        expected = np.convolve(signal, kernel, mode='full')
        return np.allclose(solution, expected, rtol=1e-5, atol=1e-8)
