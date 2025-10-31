
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

        # Calculate the length of the signal and kernel
        signal_len = len(signal)
        kernel_len = len(kernel)

        # Calculate the length of the output
        output_len = signal_len + kernel_len - 1

        # Pad the signal and kernel to the nearest power of 2 for efficient FFT
        next_power_of_two = int(2 ** np.ceil(np.log2(output_len)))
        padded_signal = np.pad(signal, (0, next_power_of_two - signal_len))
        padded_kernel = np.pad(kernel, (0, next_power_of_two - kernel_len))

        # Perform FFT on the padded signal and kernel
        fft_signal = np.fft.fft(padded_signal)
        fft_kernel = np.fft.fft(padded_kernel)

        # Multiply the FFTs of the signal and kernel
        fft_product = fft_signal * fft_kernel

        # Perform inverse FFT to get the convolution
        convolution = np.real(np.fft.ifft(fft_product))

        # Trim the convolution to the desired output length
        convolution = convolution[:output_len]

        return convolution.tolist()

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
        solution = np.array(solution)

        # Calculate the expected convolution using numpy's convolve function
        expected_convolution = np.convolve(signal, kernel, mode='full')

        # Check if the provided solution matches the expected convolution
        return np.allclose(solution, expected_convolution)
