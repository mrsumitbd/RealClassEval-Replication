
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
        sequence_a = np.array(problem['sequence_a'], dtype=np.complex128)
        sequence_b = np.array(problem['sequence_b'], dtype=np.complex128)
        convolution = np.fft.ifft(np.fft.fft(
            sequence_a) * np.fft.fft(sequence_b))
        return {'convolution': convolution.tolist()}

    def is_solution(self, problem, solution):
        """Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        sequence_a = np.array(problem['sequence_a'], dtype=np.complex128)
        sequence_b = np.array(problem['sequence_b'], dtype=np.complex128)
        expected_convolution = np.fft.ifft(
            np.fft.fft(sequence_a) * np.fft.fft(sequence_b))
        actual_convolution = np.array(
            solution['convolution'], dtype=np.complex128)
        return np.allclose(expected_convolution, actual_convolution)
