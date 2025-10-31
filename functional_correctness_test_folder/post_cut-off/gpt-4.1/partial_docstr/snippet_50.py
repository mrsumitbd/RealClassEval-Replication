
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
                - 'a': list or array of numbers (first sequence)
                - 'b': list or array of numbers (second sequence)
        Returns:
            The convolution result as a list of floats (real part only)
        '''
        a = np.array(problem['a'])
        b = np.array(problem['b'])
        n = len(a) + len(b) - 1
        n_fft = 1 << (n - 1).bit_length()
        A = np.fft.fft(a, n_fft)
        B = np.fft.fft(b, n_fft)
        C = A * B
        c = np.fft.ifft(C)
        result = np.real(c[:n])
        # If input is integer, round to nearest integer
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            result = np.rint(result).astype(int)
            return result.tolist()
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
        expected = self.solve(problem)
        # Allow for small floating point errors
        if len(expected) != len(solution):
            return False
        for x, y in zip(expected, solution):
            if isinstance(x, float) or isinstance(y, float):
                if abs(x - y) > 1e-6:
                    return False
            else:
                if x != y:
                    return False
        return True
