
import numpy as np


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
        # Extract data from the problem dictionary
        signal = problem.get('signal', np.array([]))
        kernel = problem.get('kernel', np.array([]))

        # Perform FFT on the signal and the kernel
        fft_signal = np.fft.fft(signal)
        fft_kernel = np.fft.fft(kernel, n=len(signal))

        # Multiply the FFTs element-wise
        fft_result = fft_signal * fft_kernel

        # Perform inverse FFT to get the convolution result
        result = np.fft.ifft(fft_result)

        # Return the real part of the result as the convolution
        return np.real(result)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Extract data from the problem dictionary
        signal = problem.get('signal', np.array([]))
        kernel = problem.get('kernel', np.array([]))

        # Compute the expected solution using direct convolution
        expected_solution = np.convolve(signal, kernel, mode='full')

        # Compare the lengths of the expected solution and the provided solution
        if len(expected_solution) != len(solution):
            return False

        # Check if the solutions are approximately equal
        return np.allclose(expected_solution, solution, atol=1e-5)
