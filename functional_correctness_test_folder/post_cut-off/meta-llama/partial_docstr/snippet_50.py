
import numpy as np


class FFTConvolution:

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

        # Calculate the next power of 2 for efficient FFT
        fft_len = 2 ** np.ceil(np.log2(output_len)).astype(int)

        # Pad the signal and kernel with zeros
        signal_padded = np.pad(signal, (0, fft_len - signal_len))
        kernel_padded = np.pad(kernel, (0, fft_len - kernel_len))

        # Perform FFT on the padded signal and kernel
        signal_fft = np.fft.fft(signal_padded)
        kernel_fft = np.fft.fft(kernel_padded)

        # Multiply the FFTs of the signal and kernel
        output_fft = signal_fft * kernel_fft

        # Perform inverse FFT to get the convolution output
        output = np.real(np.fft.ifft(output_fft))

        # Trim the output to the desired length
        output = output[:output_len]

        return output.tolist()

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

        # Calculate the expected output using numpy's convolve function
        expected_output = np.convolve(signal, kernel, mode='full')

        # Check if the provided solution matches the expected output
        return np.allclose(solution, expected_output)
