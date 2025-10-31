
import numpy as np


class FFTConvolution:

    def __init__(self):

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

        # Take the real part of the convolution
        solution = np.real(convolution)

        return solution

    def is_solution(self, problem, solution):

        # Compute the actual convolution using numpy's convolve function
        actual_convolution = np.convolve(
            problem['signal1'], problem['signal2'], mode='full')

        # Compare the solution with the actual convolution
        # Allow for a small tolerance due to floating point arithmetic
        return np.allclose(solution, actual_convolution, atol=1e-10)
