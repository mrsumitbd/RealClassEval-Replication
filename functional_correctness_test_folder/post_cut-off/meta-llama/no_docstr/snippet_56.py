
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:

    def __init__(self):
        pass

    def solve(self, problem):
        return fft(problem)

    def is_solution(self, problem, solution):
        reconstructed_problem = ifft(solution)
        return np.allclose(problem, reconstructed_problem)
