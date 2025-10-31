
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
                         - 'a': list or 1-D array of real numbers
                         - 'b': list or 1-D array of real numbers
        Returns:
            The solution as a list of real numbers representing the convolution of a and b
        '''
        a = np.asarray(problem.get('a', []), dtype=np.float64)
        b = np.asarray(problem.get('b', []), dtype=np.float64)

        if a.ndim != 1 or b.ndim != 1:
            raise ValueError("Inputs 'a' and 'b' must be 1-D arrays")

        # Length of the linear convolution result
        n = a.size + b.size - 1

        # Compute FFTs with zero-padding to length n
        fft_a = np.fft.fft(a, n=n)
        fft_b = np.fft.fft(b, n=n)

        # Element-wise multiplication in frequency domain
        fft_product = fft_a * fft_b

        # Inverse FFT to get convolution result
        conv = np.fft.ifft(fft_product)

        # Since inputs are real, take real part and round tiny imaginary parts
        conv_real = np.real_if_close(conv, tol=1e-10)

        # Convert to Python list for output
        return conv_real.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (list or array of real numbers)
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Convert solution to numpy array for comparison
        sol_arr = np.asarray(solution, dtype=np.float64)

        # Ensure shapes match
        if sol_arr.shape != np.asarray(expected).shape:
            return False

        # Compare with tolerance
        return np.allclose(sol_arr, expected, atol=1e-6, rtol=1e-6)
