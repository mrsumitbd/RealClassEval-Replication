
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
        signal1 = np.array(problem['signal1'])
        signal2 = np.array(problem['signal2'])
        convolution = np.real(np.fft.ifft(
            np.fft.fft(signal1) * np.fft.fft(signal2)))
        return convolution.tolist()

    def is_solution(self, problem, solution):
        """Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        signal1 = np.array(problem['signal1'])
        signal2 = np.array(problem['signal2'])
        expected_solution = np.real(np.fft.ifft(
            np.fft.fft(signal1) * np.fft.fft(signal2)))
        solution_array = np.array(solution)
        return np.allclose(solution_array, expected_solution)
