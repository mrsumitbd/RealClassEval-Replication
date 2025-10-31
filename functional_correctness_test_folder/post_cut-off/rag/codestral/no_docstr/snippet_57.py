
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
        return {'result': result.real.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Extract input arrays from the problem
        x = np.array(problem['x'])
        y = np.array(problem['y'])

        # Compute the expected convolution result
        expected_result = np.convolve(x, y, mode='full')

        # Compare with the provided solution
        provided_result = np.array(solution['result'])

        # Check if the shapes match
        if expected_result.shape != provided_result.shape:
            return False

        # Check if the values are approximately equal (allowing for floating-point precision)
        return np.allclose(expected_result, provided_result, rtol=1e-5, atol=1e-8)
