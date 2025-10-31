
import numpy as np
from scipy.fft import fft, ifft


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
        # Extract input arrays from the problem dictionary
        x = problem.get('x', np.array([]))
        y = problem.get('y', np.array([]))

        # Compute the FFT of both arrays
        fft_x = fft(x)
        fft_y = fft(y)

        # Perform element-wise multiplication in the frequency domain
        fft_result = fft_x * fft_y

        # Compute the inverse FFT to get the convolution result
        result = ifft(fft_result)

        # Return the real part of the result (imaginary part should be negligible)
        return {'result': np.real(result)}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Extract input arrays and the proposed solution
        x = problem.get('x', np.array([]))
        y = problem.get('y', np.array([]))
        result = solution.get('result', np.array([]))

        # Compute the expected convolution using numpy's convolve
        expected_result = np.convolve(x, y, mode='full')

        # Check if the proposed solution matches the expected result
        # Allow for small floating-point differences
        return np.allclose(result, expected_result, atol=1e-8)
