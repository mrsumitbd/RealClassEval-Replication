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
        a = np.array(problem['a'])
        b = np.array(problem['b'])
        n = len(a) + len(b) - 1
        nfft = 1 << (n - 1).bit_length()
        fa = np.fft.fft(a, nfft)
        fb = np.fft.fft(b, nfft)
        fc = fa * fb
        c = np.fft.ifft(fc)
        c_real = np.real(c[:n])
        # If input is integer, round to nearest integer
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            c_real = np.rint(c_real).astype(int)
            return c_real.tolist()
        return c_real.tolist()

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
        # If input is integer, round to nearest integer
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            expected = np.rint(expected).astype(int)
        return np.allclose(expected, solution, atol=1e-6)
