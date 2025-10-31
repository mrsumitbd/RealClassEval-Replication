
import numpy as np
from scipy.fftpack import fft


class FFTComplexScipyFFTpack:

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
        # Expecting problem to have key 'input' with a list of complex numbers
        x = problem['input']
        x_arr = np.array(x, dtype=np.complex128)
        result = fft(x_arr)
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
        # Compute the correct solution
        correct = self.solve(problem)
        # Compare each element with a tolerance
        if len(correct) != len(solution):
            return False
        for a, b in zip(correct, solution):
            if not np.allclose(a, b, rtol=1e-7, atol=1e-7):
                return False
        return True
