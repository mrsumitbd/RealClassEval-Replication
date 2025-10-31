
import numpy as np
from scipy.fftpack import fft


class FFTComplexScipyFFTpack:

    def __init__(self):
        pass

    def solve(self, problem):
        return fft(problem)

    def is_solution(self, problem, solution):
        return np.allclose(fft(problem), solution)
