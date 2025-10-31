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
        # Expecting problem to have keys: 'input', 'inverse' (bool)
        x = np.asarray(problem['input'])
        inverse = problem.get('inverse', False)
        if inverse:
            result = ifft(x)
        else:
            result = fft(x)
        # Return as list of complex numbers
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
        x = np.asarray(problem['input'])
        inverse = problem.get('inverse', False)
        if inverse:
            expected = ifft(x)
        else:
            expected = fft(x)
        sol = np.asarray(solution)
        # Allow for small numerical error
        return np.allclose(sol, expected, rtol=1e-5, atol=1e-8)
