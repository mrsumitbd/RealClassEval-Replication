
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:

    @staticmethod
    def solve(problem):
        return fft(problem)

    @staticmethod
    def is_solution(problem, solution):
        reconstructed = ifft(solution)
        return np.allclose(problem, reconstructed, rtol=1e-10, atol=1e-10)
