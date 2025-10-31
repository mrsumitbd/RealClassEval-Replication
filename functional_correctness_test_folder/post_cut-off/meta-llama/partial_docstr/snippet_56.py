
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
        data = problem['data']
        direction = problem.get('direction', 'forward')

        if direction == 'forward':
            solution = fft(data)
        elif direction == 'backward' or direction == 'inverse':
            solution = ifft(data)
        else:
            raise ValueError(
                "Invalid direction. It should be 'forward', 'backward', or 'inverse'.")

        return {'solution': solution.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        data = problem['data']
        direction = problem.get('direction', 'forward')

        if direction == 'forward':
            expected_solution = fft(data)
        elif direction == 'backward' or direction == 'inverse':
            expected_solution = ifft(data)
        else:
            raise ValueError(
                "Invalid direction. It should be 'forward', 'backward', or 'inverse'.")

        provided_solution = np.array(solution['solution'])

        # Compare the provided solution with the expected solution
        # We use np.allclose to account for floating point precision issues
        return np.allclose(provided_solution, expected_solution)
