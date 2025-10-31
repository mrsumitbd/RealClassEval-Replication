
import numpy as np
from scipy.fft import fft, ifft


class FFTComplexScipyFFTpack:

    @staticmethod
    def solve(problem):
        return fft(problem)

    @staticmethod
    def is_solution(problem, solution):
        reconstructed_problem = ifft(solution)
        return np.allclose(problem, reconstructed_problem)
