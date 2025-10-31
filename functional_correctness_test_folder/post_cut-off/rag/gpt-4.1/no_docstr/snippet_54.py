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
        input_h, input_w = input_matrix.shape
        kernel_h, kernel_w = kernel.shape

        out_h = input_h + kernel_h - 1
        out_w = input_w + kernel_w - 1

        # Pad input
        pad_h = kernel_h - 1
        pad_w = kernel_w - 1
        padded = np.pad(input_matrix, ((pad_h, pad_h),
                        (pad_w, pad_w)), mode='constant', constant_values=0)

        output = np.zeros(
            (out_h, out_w), dtype=np.result_type(input_matrix, kernel))

        for i in range(out_h):
            for j in range(out_w):
                region = padded[i:i+kernel_h, j:j+kernel_w]
                output[i, j] = np.sum(region * kernel)

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
        expected = self.solve(problem)
        return np.allclose(np.array(expected), np.array(solution))
