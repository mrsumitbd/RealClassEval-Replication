
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
        signal = problem.get('signal', None)
        kernel = problem.get('kernel', None)

        if signal is None or kernel is None:
            raise ValueError(
                "Signal and kernel must be provided in the problem dictionary.")

        signal_length = len(signal)
        kernel_length = len(kernel)
        fft_size = signal_length + kernel_length - 1

        signal_fft = np.fft.fft(signal, fft_size)
        kernel_fft = np.fft.fft(kernel, fft_size)

        result_fft = signal_fft * kernel_fft
        result = np.fft.ifft(result_fft).real

        return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(solution, np.ndarray):
            return False

        signal = problem.get('signal', None)
        kernel = problem.get('kernel', None)

        if signal is None or kernel is None:
            return False

        expected_length = len(signal) + len(kernel) - 1
        if len(solution) != expected_length:
            return False

        return True
