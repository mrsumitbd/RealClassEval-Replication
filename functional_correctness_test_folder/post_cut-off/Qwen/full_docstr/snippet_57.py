
import numpy as np


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        pass

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        x = problem.get('x', np.array([]))
        y = problem.get('y', np.array([]))
        if x.size == 0 or y.size == 0:
            return np.array([])
        x_fft = np.fft.fft(x)
        y_fft = np.fft.fft(y)
        conv_fft = x_fft * y_fft
        conv = np.fft.ifft(conv_fft)
        return np.real(conv)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        x = problem.get('x', np.array([]))
        y = problem.get('y', np.array([]))
        if x.size == 0 or y.size == 0:
            return solution.size == 0
        expected_solution = np.convolve(x, y, mode='full')
        return np.allclose(solution, expected_solution)
