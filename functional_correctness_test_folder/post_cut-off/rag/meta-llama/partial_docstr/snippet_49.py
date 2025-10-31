
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def solve(problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        input_array = problem['input_array']
        direction = problem.get('direction', 'forward')

        if direction == 'forward':
            output_array = fft(input_array)
        elif direction == 'backward' or direction == 'inverse':
            output_array = ifft(input_array)
        else:
            raise ValueError(
                "Invalid direction. It should be 'forward', 'backward', or 'inverse'.")

        return {'output_array': output_array}

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_array = problem['input_array']
        direction = problem.get('direction', 'forward')
        output_array = solution['output_array']

        if direction == 'forward':
            expected_output = fft(input_array)
        elif direction == 'backward' or direction == 'inverse':
            expected_output = ifft(input_array)
        else:
            return False

        # Check if the solution is valid within a tolerance
        return np.allclose(output_array, expected_output)
