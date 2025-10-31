
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
        n = len(a)
        m = len(b)
        size = n + m - 1
        # Next power of 2 for efficient FFT
        fft_size = 1 << (size - 1).bit_length()
        fa = np.fft.fft(a, fft_size)
        fb = np.fft.fft(b, fft_size)
        fc = fa * fb
        c = np.fft.ifft(fc)
        # Only take the real part and round if input is integer
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            result = np.rint(np.real(c[:size])).astype(int).tolist()
        else:
            result = np.real(c[:size]).tolist()
        return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        a = problem['a']
        b = problem['b']
        n = len(a)
        m = len(b)
        expected_size = n + m - 1
        if not isinstance(solution, list) or len(solution) != expected_size:
            return False
        # Compute direct convolution for checking
        expected = [0] * expected_size
        for i in range(n):
            for j in range(m):
                expected[i + j] += a[i] * b[j]
        # Allow for small floating point errors
        for x, y in zip(solution, expected):
            if abs(x - y) > 1e-6:
                return False
        return True
