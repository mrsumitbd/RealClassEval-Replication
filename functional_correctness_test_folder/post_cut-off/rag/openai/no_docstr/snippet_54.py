
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

    def _to_numpy(self, data):
        """Convert nested lists or numpy array to a 2D numpy array."""
        if isinstance(data, np.ndarray):
            return data
        return np.array(data, dtype=float)

    def _full_convolution(self, A, K):
        """
        Compute the full 2D convolution of A and K.
        Equivalent to scipy.signal.convolve2d(A, K, mode='full').
        """
        a_rows, a_cols = A.shape
        k_rows, k_cols = K.shape
        out_rows = a_rows + k_rows - 1
        out_cols = a_cols + k_cols - 1

        # Pad input with zeros to accommodate full convolution
        padded = np.zeros((out_rows, out_cols), dtype=float)
        padded[:a_rows, :a_cols] = A

        # Flip kernel for convolution
        K_flipped = np.flipud(np.fliplr(K))

        # Perform convolution
        out = np.zeros((out_rows, out_cols), dtype=float)
        for i in range(out_rows):
            for j in range(out_cols):
                # Compute overlap region
                i_min = max(0, i - k_rows + 1)
                i_max = min(a_rows, i + 1)
                j_min = max(0, j - k_cols + 1)
                j_max = min(a_cols, j + 1)

                # Corresponding kernel indices
                ki_min = k_rows - (i - i_min)
                ki_max = k_rows - (i - i_max) + 1
                kj_min = k_cols - (j - j_min)
                kj_max = k_cols - (j - j_max) + 1

                if i_max > i_min and j_max > j_min:
                    out[i, j] = np.sum(
                        padded[i_min:i_max, j_min:j_max] *
                        K_flipped[ki_min:ki_max, kj_min:kj_max]
                    )
        return out

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
        Returns:
            The solution in the format expected by the task
        '''
        # Extract input and kernel from problem dict
        A = self._to_numpy(problem['input'])
        K = self._to_numpy(problem['kernel'])

        # Compute full convolution
        result = self._full_convolution(A, K)

        # Convert to nested lists for consistency with expected output format
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
        # Compute expected result
        expected = self.solve(problem)

        # Convert solution to numpy array for comparison
        try:
            sol_arr = np.array(solution, dtype=float)
        except Exception:
            return False

        # Compare shapes
        if sol_arr.shape != np.array(expected).shape:
            return False

        # Use allclose for floating point tolerance
        return np.allclose(sol_arr, expected, atol=1e-6)
