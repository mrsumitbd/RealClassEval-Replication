
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
        problem: dict with keys 'input' and 'kernel', both 2D lists or np.arrays
        Returns: 2D list, the full convolution result
        '''
        input_arr = np.array(problem['input'])
        kernel = np.array(problem['kernel'])
        # Flip the kernel for convolution
        kernel = np.flipud(np.fliplr(kernel))
        in_h, in_w = input_arr.shape
        k_h, k_w = kernel.shape
        out_h = in_h + k_h - 1
        out_w = in_w + k_w - 1
        # Pad input
        pad_h = k_h - 1
        pad_w = k_w - 1
        padded = np.pad(input_arr, ((pad_h, pad_h), (pad_w, pad_w)),
                        mode='constant', constant_values=0)
        result = np.zeros((out_h, out_w), dtype=input_arr.dtype)
        for i in range(out_h):
            for j in range(out_w):
                region = padded[i:i+k_h, j:j+k_w]
                result[i, j] = np.sum(region * kernel)
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
        expected = self.solve(problem)
        # Compare shapes
        if len(expected) != len(solution):
            return False
        for row1, row2 in zip(expected, solution):
            if len(row1) != len(row2):
                return False
            for v1, v2 in zip(row1, row2):
                if v1 != v2:
                    return False
        return True
