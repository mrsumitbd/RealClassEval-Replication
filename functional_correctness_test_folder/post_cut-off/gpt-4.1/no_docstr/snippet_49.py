
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:

    @staticmethod
    def solve(problem):
        """
        problem: dict with keys:
            - 'signal': list or np.ndarray of complex numbers
            - 'inverse': bool, if True compute inverse FFT, else forward FFT
        Returns:
            - np.ndarray of complex numbers (the FFT or IFFT result)
        """
        signal = problem['signal']
        inverse = problem.get('inverse', False)
        arr = np.asarray(signal, dtype=complex)
        if inverse:
            result = ifft(arr)
        else:
            result = fft(arr)
        return result

    @staticmethod
    def is_solution(problem, solution):
        """
        Checks if the solution is the correct FFT or IFFT of the signal.
        """
        signal = problem['signal']
        inverse = problem.get('inverse', False)
        arr = np.asarray(signal, dtype=complex)
        if inverse:
            expected = ifft(arr)
        else:
            expected = fft(arr)
        sol_arr = np.asarray(solution)
        return np.allclose(sol_arr, expected, atol=1e-8)
