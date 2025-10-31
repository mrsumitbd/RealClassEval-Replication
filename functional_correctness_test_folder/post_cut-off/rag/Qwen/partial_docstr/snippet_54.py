
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
        input_array = problem['input_array']
        kernel = problem['kernel']
        mode = problem.get('mode', 'full')
        fill_value = problem.get('fill_value', 0)

        # Pad the input array with the fill value
        pad_height = kernel.shape[0] - 1
        pad_width = kernel.shape[1] - 1
        padded_array = np.pad(input_array, ((pad_height, pad_height), (
            pad_width, pad_width)), mode='constant', constant_values=fill_value)

        # Perform the convolution
        result_height = padded_array.shape[0] - kernel.shape[0] + 1
        result_width = padded_array.shape[1] - kernel.shape[1] + 1
        result = np.zeros((result_height, result_width))

        for i in range(result_height):
            for j in range(result_width):
                result[i, j] = np.sum(
                    padded_array[i:i+kernel.shape[0], j:j+kernel.shape[1]] * kernel)

        return result

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        input_array = problem['input_array']
        kernel = problem['kernel']
        mode = problem.get('mode', 'full')
        fill_value = problem.get('fill_value', 0)

        # Calculate the expected shape of the solution
        expected_height = input_array.shape[0] + kernel.shape[0] - 1
        expected_width = input_array.shape[1] + kernel.shape[1] - 1

        # Check if the solution has the expected shape
        if solution.shape != (expected_height, expected_width):
            return False

        # Recompute the solution to check correctness
        computed_solution = self.solve(problem)

        # Compare the computed solution with the provided solution
        return np.allclose(solution, computed_solution)
