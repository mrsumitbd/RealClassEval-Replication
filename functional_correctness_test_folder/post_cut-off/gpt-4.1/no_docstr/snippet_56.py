
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        problem: dict with keys:
            - 'input': list or np.ndarray of complex numbers
            - 'inverse': bool, if True compute inverse FFT, else FFT
        Returns:
            np.ndarray of complex numbers (the FFT or IFFT result)
        """
        x = np.asarray(problem['input'], dtype=complex)
        inverse = problem.get('inverse', False)
        if inverse:
            result = ifft(x)
        else:
            result = fft(x)
        return result

    def is_solution(self, problem, solution):
        """
        Checks if the solution is the correct FFT or IFFT of the input.
        Uses np.allclose for numerical tolerance.
        """
        x = np.asarray(problem['input'], dtype=complex)
        inverse = problem.get('inverse', False)
        if inverse:
            expected = ifft(x)
        else:
            expected = fft(x)
        solution = np.asarray(solution)
        return np.allclose(solution, expected)
