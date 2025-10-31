
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
        input_array = problem.get('input_array')
        kernel = problem.get('kernel')

        if input_array is None or kernel is None:
            raise ValueError(
                "Both 'input_array' and 'kernel' must be provided in the problem.")

        input_array = np.array(input_array)
        kernel = np.array(kernel)

        # Perform full convolution
        solution = np.zeros((input_array.shape[0] + kernel.shape[0] - 1,
                             input_array.shape[1] + kernel.shape[1] - 1))

        for i in range(solution.shape[0]):
            for j in range(solution.shape[1]):
                # Calculate the overlapping region
                input_i_start = max(0, i - kernel.shape[0] + 1)
                input_i_end = min(input_array.shape[0], i + 1)
                input_j_start = max(0, j - kernel.shape[1] + 1)
                input_j_end = min(input_array.shape[1], j + 1)

                kernel_i_start = max(0, kernel.shape[0] - 1 - i)
                kernel_i_end = min(
                    kernel.shape[0], kernel.shape[0] - 1 - i + input_array.shape[0])
                kernel_j_start = max(0, kernel.shape[1] - 1 - j)
                kernel_j_end = min(
                    kernel.shape[1], kernel.shape[1] - 1 - j + input_array.shape[1])

                # Perform element-wise multiplication and sum
                solution[i, j] = np.sum(input_array[input_i_start:input_i_end, input_j_start:input_j_end] *
                                        kernel[kernel_i_start:kernel_i_end, kernel_j_start:kernel_j_end])

        return solution.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(solution, list) or not all(isinstance(row, list) for row in solution):
            return False

        input_array = problem.get('input_array')
        kernel = problem.get('kernel')

        if input_array is None or kernel is None:
            return False

        input_array = np.array(input_array)
        kernel = np.array(kernel)
        solution = np.array(solution)

        # Check if the solution has the correct shape
        expected_shape = (input_array.shape[0] + kernel.shape[0] - 1,
                          input_array.shape[1] + kernel.shape[1] - 1)
        if solution.shape != expected_shape:
            return False

        # Verify the solution by comparing with a reference implementation
        reference_solution = np.convolve(input_array.flatten(
        ), kernel.flatten(), mode='full').reshape(expected_shape)

        return np.allclose(solution, reference_solution, atol=1e-6)
