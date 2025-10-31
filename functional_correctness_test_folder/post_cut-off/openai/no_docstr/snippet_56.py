
import numpy as np
from scipy.fftpack import fft


class FFTComplexScipyFFTpack:
    def __init__(self):
        pass

    def solve(self, problem):
        """
        Compute the complex FFT of the input data using scipy.fftpack.

        Parameters
        ----------
        problem : dict
            Must contain a key 'data' with a sequence or array of complex numbers.

        Returns
        -------
        numpy.ndarray
            The FFT of the input data.
        """
        data = problem.get('data')
        if data is None:
            raise ValueError("Problem must contain a 'data' key.")
        return fft(np.asarray(data))

    def is_solution(self, problem, solution):
        """
        Verify that the provided solution matches the expected FFT result.

        Parameters
        ----------
        problem : dict
            May contain 'data' and optionally 'expected'.
        solution : array-like
            The FFT result to validate.

        Returns
        -------
        bool
            True if the solution matches the expected result within tolerance.
        """
        data = problem.get('data')
        if data is None:
            return False

        expected = problem.get('expected')
        if expected is None:
            expected = fft(np.asarray(data))

        return np.allclose(solution, expected, atol=1e-6, rtol=1e-6)
