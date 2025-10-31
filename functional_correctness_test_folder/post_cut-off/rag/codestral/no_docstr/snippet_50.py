
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
        # Extract input arrays from the problem
        x = np.array(problem['x'])
        y = np.array(problem['y'])

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
        # Extract input arrays and the solution
        x = np.array(problem['x'])
        y = np.array(problem['y'])
        result = np.array(solution['result'])

        # Compute the direct convolution for comparison
        direct_conv = np.convolve(x, y, mode='full')

        # Check if the solution matches the direct convolution result
        # Allow for small numerical differences due to floating-point precision
        return np.allclose(result, direct_conv, atol=1e-10)
