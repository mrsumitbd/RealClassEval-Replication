
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

        # Take the real part to get rid of any imaginary components
        solution = np.real(convolution)

        return solution

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

        # Compute the direct convolution
        direct_convolution = np.convolve(signal1, signal2)

        # Compare the solution with the direct convolution
        # Allow for a small tolerance due to floating point arithmetic
        if np.allclose(solution, direct_convolution, atol=1e-10):
            return True
        else:
            return False
