
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
            return None

        signal_length = len(signal)
        kernel_length = len(kernel)

        # Zero-padding
        fft_size = signal_length + kernel_length - 1
        signal_padded = np.pad(
            signal, (0, fft_size - signal_length), 'constant')
        kernel_padded = np.pad(
            kernel, (0, fft_size - kernel_length), 'constant')

        # FFT
        signal_fft = np.fft.fft(signal_padded)
        kernel_fft = np.fft.fft(kernel_padded)

        # Element-wise multiplication
        result_fft = signal_fft * kernel_fft

        # Inverse FFT
        result = np.fft.ifft(result_fft).real

        # Truncate to the correct length
        result = result[:signal_length + kernel_length - 1]

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
        if solution is None:
            return False

        signal = problem.get('signal', None)
        kernel = problem.get('kernel', None)

        if signal is None or kernel is None:
            return False

        expected_length = len(signal) + len(kernel) - 1
        if len(solution) != expected_length:
            return False

        # Check if the solution matches a direct convolution (for small inputs)
        if len(signal) < 100 and len(kernel) < 100:
            direct_conv = np.convolve(signal, kernel)
            return np.allclose(solution, direct_conv, rtol=1e-5, atol=1e-8)

        return True
