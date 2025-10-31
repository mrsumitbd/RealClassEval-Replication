from scipy import signal
import logging
import numpy as np

class Convolve2DFullFill:
    """
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the Convolve2DFullFill."""
        self.mode = 'full'
        self.boundary = 'fill'

    def solve(self, problem):
        """
        Compute the 2D convolution of arrays a and b using "full" mode and "fill" boundary.
        Uses scipy.signal.fftconvolve for efficiency, which implicitly handles "fill" boundary.

        Args:
            problem: A tuple (a, b) of 2D arrays.

        Returns:
            A 2D array containing the convolution result.
        """
        try:
            a, b = problem
            if not (isinstance(a, np.ndarray) and a.dtype == np.float32):
                a = np.asarray(a, dtype=np.float32)
            if not (isinstance(b, np.ndarray) and b.dtype == np.float32):
                b = np.asarray(b, dtype=np.float32)
            result = signal.fftconvolve(a, b, mode=self.mode)
            return result
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
            a, b = problem
            reference = signal.convolve2d(a, b, mode=self.mode, boundary=self.boundary)
            tol = 1e-06
            error = np.linalg.norm(solution - reference) / (np.linalg.norm(reference) + 1e-12)
            if error > tol:
                logging.error(f'Convolve2D solution error {error} exceeds tolerance {tol}.')
                return False
            return True
        except Exception as e:
            logging.error(f'Error in is_solution method: {e}')
            return False