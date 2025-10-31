
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:

    @staticmethod
    def solve(problem):
        return fft(problem)

    @staticmethod
    def is_solution(problem, solution):
        return np.allclose(problem, ifft(solution))
