
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:

    @staticmethod
    def solve(problem):
        """Solve the given FFT problem using scipy's FFTPACK."""
        return fft(problem)

    @staticmethod
    def is_solution(problem, solution):
        """Check if the given solution is correct by comparing the inverse FFT of the solution with the original problem."""
        # Calculate the inverse FFT of the solution
        reconstructed_problem = ifft(solution)

        # Compare the reconstructed problem with the original problem
        # We use np.allclose to account for floating point precision errors
        return np.allclose(problem, reconstructed_problem)
