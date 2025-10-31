
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
        a = np.array(problem['a'])
        b = np.array(problem['b'])

        n = len(a) + len(b) - 1
        fft_a = np.fft.fft(a, n)
        fft_b = np.fft.fft(b, n)
        fft_result = fft_a * fft_b
        result = np.fft.ifft(fft_result).real

        return result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        a = np.array(problem['a'])
        b = np.array(problem['b'])

        expected = np.convolve(a, b)
        actual = np.array(solution)

        return np.allclose(expected, actual, rtol=1e-5, atol=1e-8)
