
import numpy as np


class FFTConvolution:
    """Initial implementation of fft_convolution task.

    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the FFTConvolution."""
        pass

    def solve(self, problem):
        """Solve the fft_convolution problem.

        Args:
            problem: Dictionary containing problem data specific to fft_convolution

        Returns:
            The solution in the format expected by the task
        """
        sequence1 = np.array(problem['sequence1'], dtype=np.complex128)
        sequence2 = np.array(problem['sequence2'], dtype=np.complex128)
        convolution = np.fft.ifft(np.fft.fft(
            sequence1) * np.fft.fft(sequence2))
        return {'convolution': convolution.tolist()}

    def is_solution(self, problem, solution):
        """Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        sequence1 = np.array(problem['sequence1'], dtype=np.complex128)
        sequence2 = np.array(problem['sequence2'], dtype=np.complex128)
        expected_convolution = np.fft.ifft(
            np.fft.fft(sequence1) * np.fft.fft(sequence2))
        provided_convolution = np.array(
            solution['convolution'], dtype=np.complex128)
        return np.allclose(expected_convolution, provided_convolution)
