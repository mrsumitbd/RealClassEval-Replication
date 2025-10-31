
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
                "Both input_array and kernel must be provided in the problem.")

        input_array = np.array(input_array)
        kernel = np.array(kernel)

        # Perform full convolution
        solution = np.zeros((input_array.shape[0] + kernel.shape[0] - 1,
                            input_array.shape[1] + kernel.shape[1] - 1))

        for i in range(solution.shape[0]):
            for j in range(solution.shape[1]):
                # Calculate the overlapping region
                input_start_i = max(0, i - kernel.shape[0] + 1)
                input_end_i = min(input_array.shape[0], i + 1)
                input_start_j = max(0, j - kernel.shape[1] + 1)
                input_end_j = min(input_array.shape[1], j + 1)

                kernel_start_i = max(0, kernel.shape[0] - 1 - i)
                kernel_end_i = min(
                    kernel.shape[0], kernel.shape[0] - 1 - (i - input_array.shape[0] + 1))
                kernel_start_j = max(0, kernel.shape[1] - 1 - j)
                kernel_end_j = min(
                    kernel.shape[1], kernel.shape[1] - 1 - (j - input_array.shape[1] + 1))

                # Perform element-wise multiplication and sum
                solution[i, j] = np.sum(
                    input_array[input_start_i:input_end_i, input_start_j:input_end_j] *
                    kernel[kernel_start_i:kernel_end_i,
                           kernel_start_j:kernel_end_j]
                )

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
        if solution is None:
            return False

        input_array = np.array(problem.get('input_array'))
        kernel = np.array(problem.get('kernel'))
        expected_solution = np.array(solution)

        # Check if the solution has the correct shape
        if expected_solution.shape != (input_array.shape[0] + kernel.shape[0] - 1,
                                       input_array.shape[1] + kernel.shape[1] - 1):
            return False

        # Check if the solution matches the expected result
        actual_solution = self.solve(problem)
        return np.allclose(expected_solution, actual_solution, atol=1e-6)
