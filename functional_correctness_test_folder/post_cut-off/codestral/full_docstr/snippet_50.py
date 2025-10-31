
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
        Returns:
            The solution in the format expected by the task
        '''
        signal1 = problem['signal1']
        signal2 = problem['signal2']

        # Compute the FFT of both signals
        fft1 = np.fft.fft(signal1)
        fft2 = np.fft.fft(signal2)

        # Multiply the FFTs
        fft_product = fft1 * fft2

        # Compute the inverse FFT to get the convolution
        convolution = np.fft.ifft(fft_product)

        # Return the real part of the convolution
        return {'convolution': np.real(convolution)}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        signal1 = problem['signal1']
        signal2 = problem['signal2']
        convolution = solution['convolution']

        # Compute the direct convolution for comparison
        direct_convolution = np.convolve(signal1, signal2, mode='full')

        # Check if the computed convolution matches the direct convolution
        return np.allclose(convolution, direct_convolution, atol=1e-6)
