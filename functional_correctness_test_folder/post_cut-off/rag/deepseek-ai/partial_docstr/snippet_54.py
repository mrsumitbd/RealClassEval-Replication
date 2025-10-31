
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
        input_matrix = problem['input_matrix']
        kernel = problem['kernel']
        output_shape = (
            input_matrix.shape[0] + kernel.shape[0] - 1,
            input_matrix.shape[1] + kernel.shape[1] - 1
        )
        output = np.zeros(output_shape)

        # Pad the input matrix with zeros
        padded_input = np.pad(
            input_matrix,
            (
                (kernel.shape[0] - 1, kernel.shape[0] - 1),
                (kernel.shape[1] - 1, kernel.shape[1] - 1)
            ),
            mode='constant'
        )

        # Perform convolution
        for i in range(output_shape[0]):
            for j in range(output_shape[1]):
                output[i, j] = np.sum(
                    padded_input[i:i+kernel.shape[0],
                                 j:j+kernel.shape[1]] * kernel
                )

        return output

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Compare against reference implementation (scipy.signal.convolve2d with 'full' mode)
        try:
            from scipy.signal import convolve2d
            reference = convolve2d(
                problem['input_matrix'], problem['kernel'], mode='full')
            return np.allclose(solution, reference)
        except ImportError:
            # Fallback to manual validation if scipy is not available
            output_shape = (
                problem['input_matrix'].shape[0] +
                problem['kernel'].shape[0] - 1,
                problem['input_matrix'].shape[1] +
                problem['kernel'].shape[1] - 1
            )
            if solution.shape != output_shape:
                return False
            # Additional checks could be added here if needed
            return True
