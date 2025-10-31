import logging
import scipy.fftpack as fftpack
import numpy as np

class FFTComplexScipyFFTpack:
    """
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the FFTComplexScipyFFTpack."""
        pass

    def solve(self, problem):
        """
        Solve the fft_cmplx_scipy_fftpack problem.

        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack

        Returns:
            The solution in the format expected by the task
        """
        try:
            '\n            Compute the N-dimensional FFT using scipy.fftpack.\n            '
            return fftpack.fftn(problem)
        except Exception as e:
            logging.error(f'Error in solve method: {e}')
            raise e

    def is_solution(self, problem, solution):
        """
        Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        try:
            "\n            Check if the FFT solution is valid and optimal.\n\n            A valid solution must match the reference implementation (numpy's FFT)\n            within a small tolerance.\n\n            :param problem: Input complex array.\n            :param solution: Computed FFT result.\n            :return: True if the solution is valid and optimal, False otherwise.\n            "
            tol = 1e-06
            reference = np.fft.fftn(problem)
            error = np.linalg.norm(solution - reference) / (np.linalg.norm(reference) + 1e-12)
            if error > tol:
                logging.error(f'FFT solution error {error} exceeds tolerance {tol}.')
                return False
            return True
        except Exception as e:
            logging.error(f'Error in is_solution method: {e}')
            return False