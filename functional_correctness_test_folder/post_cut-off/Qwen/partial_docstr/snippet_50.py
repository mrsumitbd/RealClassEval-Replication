
import numpy as np


class FFTConvolution:

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
        h = problem.get('h', np.array([]))
        if x.size == 0 or h.size == 0:
            return np.array([])
        X = np.fft.fft(x)
        H = np.fft.fft(h, n=len(x) + len(h) - 1)
        y = np.fft.ifft(X * H)
        return np.real(y)

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
        h = problem.get('h', np.array([]))
        if x.size == 0 or h.size == 0:
            return solution.size == 0
        expected_solution = np.convolve(x, h)
        return np.allclose(solution, expected_solution)
