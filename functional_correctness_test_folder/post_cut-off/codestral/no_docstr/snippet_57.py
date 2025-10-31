
import numpy as np


class FFTConvolution:

    def __init__(self):

        pass

    def solve(self, problem):

        f, g = problem
        f_fft = np.fft.fft(f)
        g_fft = np.fft.fft(g)
        h_fft = f_fft * g_fft
        h = np.fft.ifft(h_fft)
        return h

    def is_solution(self, problem, solution):

        f, g = problem
        h = solution
        f_padded = np.pad(f, (0, len(g) - 1))
        g_padded = np.pad(g, (0, len(f) - 1))
        h_expected = np.convolve(f_padded, g_padded)
        return np.allclose(h, h_expected)
