
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

        fft_size = signal_length + kernel_length - 1

        signal_fft = np.fft.fft(signal, fft_size)
        kernel_fft = np.fft.fft(kernel, fft_size)

        result_fft = signal_fft * kernel_fft
        result = np.fft.ifft(result_fft).real

        return result.tolist()

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

        expected_result = np.convolve(signal, kernel, mode='full')
        solution_array = np.array(solution)

        return np.allclose(solution_array, expected_result, rtol=1e-5, atol=1e-8)
