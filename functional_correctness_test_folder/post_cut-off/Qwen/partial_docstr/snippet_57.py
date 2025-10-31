
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
        # Assuming problem contains 'signal' and 'kernel' as keys
        signal = problem['signal']
        kernel = problem['kernel']

        # Perform FFT on the signal and kernel
        fft_signal = np.fft.fft(signal)
        fft_kernel = np.fft.fft(kernel, n=len(signal))

        # Multiply the FFTs element-wise
        fft_result = fft_signal * fft_kernel

        # Perform inverse FFT to get the convolution result
        result = np.fft.ifft(fft_result)

        # Return the real part of the result as the convolution
        return np.real(result)

    def is_solution(self, problem, solution):
        # Directly compute the convolution using np.convolve for comparison
        signal = problem['signal']
        kernel = problem['kernel']
        direct_solution = np.convolve(signal, kernel, mode='full')

        # Compare the solutions
        return np.allclose(solution, direct_solution, atol=1e-6)
