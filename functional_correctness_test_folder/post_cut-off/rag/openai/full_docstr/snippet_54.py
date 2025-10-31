
import numpy as np


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
                     Expected keys:
                         - 'input': 2D array-like (list of lists or np.ndarray)
                         - 'kernel': 2D array-like (list of lists or np.ndarray)
        Returns:
            The solution as a 2D list of numbers (same type as input elements)
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")

        if 'input' not in problem or 'kernel' not in problem:
            raise KeyError("problem must contain 'input' and 'kernel' keys")

        # Convert to numpy arrays
        A = np.array(problem['input'])
        B = np.array(problem['kernel'])

        if A.ndim != 2 or B.ndim != 2:
            raise ValueError("both 'input' and 'kernel' must be 2D")

        m, n = A.shape
        k, l = B.shape

        # Output size for full convolution
        out_rows = m + k - 1
        out_cols = n + l - 1

        # Pad input with zeros on all sides
        pad_top = k - 1
        pad_left = l - 1
        padded = np.pad(A, ((pad_top, pad_top), (pad_left, pad_left)),
                        mode='constant', constant_values=0)

        # Compute convolution
        out = np.zeros((out_rows, out_cols), dtype=A.dtype)

        for i in range(out_rows):
            for j in range(out_cols):
                # Element-wise multiplication and sum
                sub = padded[i:i + k, j:j + l]
                out[i, j] = np.sum(sub * B)

        # Convert to list of lists for consistency
        return out.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dict
            solution: The proposed solution (2D list or np.ndarray)
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Convert solution to numpy array for comparison
        try:
            sol_arr = np.array(solution)
        except Exception:
            return False

        exp_arr = np.array(expected)

        # Use allclose for numeric tolerance
        return np.allclose(sol_arr, exp_arr, atol=1e-8)
