
import numpy as np


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
                     Expected keys:
                         - "input": 2D array-like (list of lists or np.ndarray)
                         - "kernel": 2D array-like (list of lists or np.ndarray)
        Returns:
            The solution in the format expected by the task
            (a 2D numpy array with the full convolution result)
        '''
        # Extract input and kernel
        inp = np.asarray(problem.get('input'), dtype=float)
        ker = np.asarray(problem.get('kernel'), dtype=float)

        if inp.ndim != 2 or ker.ndim != 2:
            raise ValueError("Both input and kernel must be 2D arrays.")

        # Dimensions
        m, n = inp.shape
        k, l = ker.shape

        # Output shape for full convolution
        out_shape = (m + k - 1, n + l - 1)
        out = np.zeros(out_shape, dtype=float)

        # Pad input with zeros on all sides
        padded = np.pad(inp, ((k - 1, k - 1), (l - 1, l - 1)),
                        mode='constant', constant_values=0)

        # Perform convolution via sliding window
        for i in range(out_shape[0]):
            for j in range(out_shape[1]):
                # Element-wise multiplication and sum
                sub = padded[i:i + k, j:j + l]
                out[i, j] = np.sum(sub * ker)

        return out

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution (2D array-like)
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Compute expected solution
        expected = self.solve(problem)

        # Convert provided solution to numpy array
        sol_arr = np.asarray(solution, dtype=float)

        # Compare shapes
        if expected.shape != sol_arr.shape:
            return False

        # Use allclose for floating point tolerance
        return np.allclose(expected, sol_arr, atol=1e-6)
