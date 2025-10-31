
import numpy as np


class FFTConvolution:

    def __init__(self):
        pass

    def solve(self, problem):
        # Assuming problem is a tuple of two arrays (a, b) to convolve
        a, b = problem
        # Compute the FFT of both arrays
        fft_a = np.fft.fft(a)
        fft_b = np.fft.fft(b)
        # Multiply the FFTs element-wise
        fft_result = fft_a * fft_b
        # Compute the inverse FFT to get the convolution result
        result = np.fft.ifft(fft_result)
        # Return the real part of the result, as the imaginary part should be negligible
        return np.real(result)

    def is_solution(self, problem, solution):
        # Compute the true convolution using numpy's convolve function for comparison
        a, b = problem
        true_solution = np.convolve(a, b, mode='full')
        # Check if the provided solution matches the true solution within a tolerance
        return np.allclose(solution, true_solution)
