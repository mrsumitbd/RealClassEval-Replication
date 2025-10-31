
import numpy as np


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
                     Expected keys:
                         - 'a': list or 1-D array of numbers
                         - 'b': list or 1-D array of numbers
        Returns:
            The solution as a list of numbers representing the linear convolution
            of a and b.
        '''
        a = np.asarray(problem['a'], dtype=np.float64)
        b = np.asarray(problem['b'], dtype=np.float64)

        # Length of the linear convolution
        n = a.size + b.size - 1

        # Compute FFTs with zero-padding to length n
        fft_a = np.fft.fft(a, n)
        fft_b = np.fft.fft(b, n)

        # Element-wise multiplication in frequency domain
        fft_product = fft_a * fft_b

        # Inverse FFT to get convolution result
        conv = np.fft.ifft(fft_product)

        # Since input is real, imaginary part should be negligible
        conv_real = np.real(conv)

        # If the inputs were integers, round to nearest integer
        if np.issubdtype(a.dtype, np.integer) and np.issubdtype(b.dtype, np.integer):
            conv_real = np.rint(conv_real)

        # Return as a plain Python list
        return conv_real.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (list or array)
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Compute expected convolution using the same method as solve
        expected = self.solve(problem)

        # Convert solution to numpy array for comparison
        sol_arr = np.asarray(solution, dtype=np.float64)

        # Use a tolerance for floating point comparison
        return np.allclose(sol_arr, expected, atol=1e-6)
