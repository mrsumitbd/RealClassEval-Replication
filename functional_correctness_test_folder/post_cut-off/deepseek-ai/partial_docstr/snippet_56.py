
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:

    def __init__(self):
        '''Initialize the FFTComplexScipyFFTpack.'''
        pass

    def solve(self, problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        input_data = problem['input']
        transform_type = problem.get('transform_type', 'fft')

        if transform_type == 'fft':
            solution = fft(input_data)
        elif transform_type == 'ifft':
            solution = ifft(input_data)
        else:
            raise ValueError(
                "Invalid transform_type. Must be 'fft' or 'ifft'.")

        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_data = problem['input']
        transform_type = problem.get('transform_type', 'fft')

        if transform_type == 'fft':
            expected_solution = fft(input_data)
        elif transform_type == 'ifft':
            expected_solution = ifft(input_data)
        else:
            return False

        return np.allclose(solution, expected_solution)
