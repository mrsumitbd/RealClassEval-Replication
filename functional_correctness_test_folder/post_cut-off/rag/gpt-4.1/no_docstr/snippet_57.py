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
        # If input is integer, round result
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            c = np.rint(c).astype(int)
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
        n = len(a) + len(b) - 1
        n_fft = 1 << (n - 1).bit_length()
        fa = np.fft.fft(a, n_fft)
        fb = np.fft.fft(b, n_fft)
        fc = fa * fb
        c = np.fft.ifft(fc)
        c = np.real(c[:n])
        # If input is integer, round result
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            c = np.rint(c).astype(int)
        expected = c.tolist()
        # Allow small floating point error for float input
        if isinstance(expected[0], float):
            return all(np.isclose(x, y, atol=1e-6) for x, y in zip(expected, solution))
        else:
            return expected == solution
