
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
        Returns:
            The solution in the format expected by the task
        '''
        input_matrix = np.array(problem['input'])
        kernel = np.array(problem['kernel'])
        # Full convolution: output shape is (N+K-1, M+L-1)
        output_shape = (
            input_matrix.shape[0] + kernel.shape[0] - 1,
            input_matrix.shape[1] + kernel.shape[1] - 1
        )
        # Pad input
        pad_height = kernel.shape[0] - 1
        pad_width = kernel.shape[1] - 1
        padded_input = np.pad(input_matrix, ((pad_height, pad_height),
                              (pad_width, pad_width)), mode='constant', constant_values=0)
        # Flip kernel
        flipped_kernel = np.flipud(np.fliplr(kernel))
        # Convolve
        result = np.zeros(output_shape, dtype=input_matrix.dtype)
        for i in range(output_shape[0]):
            for j in range(output_shape[1]):
                region = padded_input[i:i+kernel.shape[0], j:j+kernel.shape[1]]
                result[i, j] = np.sum(region * flipped_kernel)
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
        # Allow for integer/float comparison tolerance
        arr1 = np.array(expected)
        arr2 = np.array(solution)
        if arr1.shape != arr2.shape:
            return False
        return np.allclose(arr1, arr2)
