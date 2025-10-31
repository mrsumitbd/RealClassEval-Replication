
import numpy as np
from scipy.fftpack import fft, ifft


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

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
        input_array = problem['input']
        direction = problem.get('direction', 'forward')
        if direction == 'forward':
            solution = fft(input_array)
        elif direction == 'backward' or direction == 'inverse':
            solution = ifft(input_array)
        else:
            raise ValueError(
                'Invalid direction. It should be "forward" or "backward"/"inverse".')
        return {'output': solution}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_array = problem['input']
        direction = problem.get('direction', 'forward')
        if direction == 'forward':
            expected_solution = fft(input_array)
        elif direction == 'backward' or direction == 'inverse':
            expected_solution = ifft(input_array)
        else:
            raise ValueError(
                'Invalid direction. It should be "forward" or "backward"/"inverse".')
        provided_solution = solution['output']
        return np.allclose(expected_solution, provided_solution)
