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
        n_fft = 1 << (n - 1).bit_length()
        fa = np.fft.fft(a, n_fft)
        fb = np.fft.fft(b, n_fft)
        fc = fa * fb
        c = np.fft.ifft(fc)
        c = np.real(c[:n])
        # If input is integer, round output
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            c = np.round(c).astype(int)
            return c.tolist()
        return c.tolist()

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
        sol = np.array(solution)
        if expected.shape != sol.shape:
            return False
        # If input is integer, compare as integer
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            return np.all(expected == sol)
        return np.allclose(expected, sol, atol=1e-8)
