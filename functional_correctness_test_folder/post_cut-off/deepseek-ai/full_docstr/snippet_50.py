
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
        signal = np.array(problem['signal'])
        kernel = np.array(problem['kernel'])

        signal_length = len(signal)
        kernel_length = len(kernel)
        output_length = signal_length + kernel_length - 1

        fft_size = 1 << (2 * output_length - 1).bit_length()

        signal_fft = np.fft.fft(signal, fft_size)
        kernel_fft = np.fft.fft(kernel, fft_size)

        convolved_fft = signal_fft * kernel_fft
        convolved = np.fft.ifft(convolved_fft).real[:output_length]

        return convolved.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        signal = np.array(problem['signal'])
        kernel = np.array(problem['kernel'])

        expected_output = np.convolve(signal, kernel)
        actual_output = np.array(solution)

        return np.allclose(expected_output, actual_output, atol=1e-6)
