
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
        a = np.array(problem['a'])
        b = np.array(problem['b'])

        # Compute the FFT of both signals
        fft_a = np.fft.fft(a)
        fft_b = np.fft.fft(b)

        # Multiply the FFTs element-wise
        fft_result = fft_a * fft_b

        # Compute the inverse FFT to get the convolution result
        result = np.fft.ifft(fft_result).real

        return result.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the solution is correct.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
            solution: The proposed solution to verify
        Returns:
            bool: True if the solution is correct, False otherwise
        '''
        a = np.array(problem['a'])
        b = np.array(problem['b'])

        # Compute the ground truth convolution using numpy's convolve
        expected = np.convolve(a, b, mode='full')

        # Compare the solution with the expected result, allowing for small numerical errors
        return np.allclose(solution, expected, rtol=1e-5, atol=1e-8)
