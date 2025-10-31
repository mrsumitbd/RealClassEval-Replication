import numpy as np
import logging
from scipy import signal
from scipy.fft import next_fast_len

class FFTConvolution:
    """
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the FFTConvolution."""
        pass

    def solve(self, problem):
        """
        Solve the fft_convolution problem.

        Args:
            problem: Dictionary containing problem data specific to fft_convolution

        Returns:
            The solution in the format expected by the task
        """
        try:
            '\n            Solve the convolution problem using a manual Fast Fourier Transform approach.\n            This implementation is optimized for performance by using rfft for real signals\n            and choosing an efficient FFT length.\n\n            :param problem: A dictionary representing the convolution problem.\n            :return: A dictionary with key:\n                     "convolution": a list representing the convolution result.\n            '
            signal_x = np.array(problem['signal_x'])
            signal_y = np.array(problem['signal_y'])
            mode = problem.get('mode', 'full')
            len_x = len(signal_x)
            len_y = len(signal_y)
            if min(len_x, len_y) == 0:
                return {'convolution': []}
            n = len_x + len_y - 1
            fft_size = next_fast_len(n)
            fft_x = np.fft.rfft(signal_x, n=fft_size)
            fft_y = np.fft.rfft(signal_y, n=fft_size)
            fft_conv = fft_x * fft_y
            full_convolution = np.fft.irfft(fft_conv, n=fft_size)
            if mode == 'full':
                convolution_result = full_convolution[:n]
            elif mode == 'same':
                start = (len_y - 1) // 2
                convolution_result = full_convolution[start:start + len_x]
            elif mode == 'valid':
                valid_len = max(0, max(len_x, len_y) - min(len_x, len_y) + 1)
                if len_x >= len_y:
                    start = len_y - 1
                    convolution_result = full_convolution[start:start + valid_len]
                else:
                    start = len_x - 1
                    convolution_result = full_convolution[start:start + valid_len]
            else:
                raise ValueError(f'Invalid mode: {mode}')
            solution = {'convolution': convolution_result.tolist()}
            return solution
        except Exception as e:
            logging.error(f'Error in solve method: {e}')
            raise e

    def is_solution(self, problem, solution):
        """
        Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        try:
            '\n            Validate the FFT convolution solution.\n\n            Checks:\n            - Solution contains the key \'convolution\'.\n            - The result is a list of numbers.\n            - The result is numerically close to the reference solution computed using scipy.signal.fftconvolve.\n            - The length of the result matches the expected length for the given mode.\n\n            :param problem: Dictionary representing the convolution problem.\n            :param solution: Dictionary containing the solution with key "convolution".\n            :return: True if the solution is valid and accurate, False otherwise.\n            '
            if 'convolution' not in solution:
                logging.error("Solution missing 'convolution' key.")
                return False
            student_result = solution['convolution']
            if not isinstance(student_result, list):
                logging.error('Convolution result must be a list.')
                return False
            try:
                student_result_np = np.array(student_result, dtype=float)
                if not np.all(np.isfinite(student_result_np)):
                    logging.error('Convolution result contains non-finite values (NaN or inf).')
                    return False
            except ValueError:
                logging.error('Could not convert convolution result to a numeric numpy array.')
                return False
            signal_x = np.array(problem['signal_x'])
            signal_y = np.array(problem['signal_y'])
            mode = problem.get('mode', 'full')
            len_x = len(signal_x)
            len_y = len(signal_y)
            if mode == 'full':
                expected_len = len_x + len_y - 1
            elif mode == 'same':
                expected_len = len_x
            elif mode == 'valid':
                expected_len = max(0, max(len_x, len_y) - min(len_x, len_y) + 1)
            else:
                logging.error(f'Invalid mode provided in problem: {mode}')
                return False
            if len_x == 0 or len_y == 0:
                expected_len = 0
            if len(student_result_np) != expected_len:
                logging.error(f"Incorrect result length for mode '{mode}'. Expected {expected_len}, got {len(student_result_np)}.")
                return False
            try:
                reference_result = signal.fftconvolve(signal_x, signal_y, mode=mode)
            except Exception as e:
                logging.error(f'Error calculating reference solution: {e}')
                return False
            if expected_len == 0:
                if len(student_result_np) == 0:
                    return True
                else:
                    logging.error('Expected empty result for empty input, but got non-empty result.')
                    return False
            abs_tol = 1e-06
            rel_tol = 1e-06
            is_close = np.allclose(student_result_np, reference_result, rtol=rel_tol, atol=abs_tol)
            if not is_close:
                diff = np.abs(student_result_np - reference_result)
                max_diff = np.max(diff) if len(diff) > 0 else 0
                avg_diff = np.mean(diff) if len(diff) > 0 else 0
                logging.error(f'Numerical difference between student solution and reference exceeds tolerance. Max diff: {max_diff:.2e}, Avg diff: {avg_diff:.2e} (atol={abs_tol}, rtol={rel_tol}).')
                return False
            return True
        except Exception as e:
            logging.error(f'Error in is_solution method: {e}')
            return False