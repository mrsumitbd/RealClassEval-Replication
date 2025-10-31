
import numpy as np
from scipy.signal import convolve2d


class Convolve2DFullFill:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Convolve the given 2D array with the given kernel.

        Args:
        problem (dict): A dictionary containing 'array' and 'kernel'.

        Returns:
        np.ndarray: The result of the convolution operation.
        """
        array = problem['array']
        kernel = problem['kernel']
        return convolve2d(array, kernel, mode='full', fillvalue=0)

    def is_solution(self, problem, solution):
        """
        Check if the given solution is correct.

        Args:
        problem (dict): A dictionary containing 'array' and 'kernel'.
        solution (np.ndarray): The proposed solution.

        Returns:
        bool: True if the solution is correct, False otherwise.
        """
        array = problem['array']
        kernel = problem['kernel']
        expected_solution = convolve2d(array, kernel, mode='full', fillvalue=0)
        return np.array_equal(solution, expected_solution)


# Example usage:
if __name__ == "__main__":
    convolve_solver = Convolve2DFullFill()

    # Define a problem
    array = np.array([[1, 2], [3, 4]])
    kernel = np.array([[0, 1], [1, 0]])
    problem = {'array': array, 'kernel': kernel}

    # Solve the problem
    solution = convolve_solver.solve(problem)
    print("Solution:")
    print(solution)

    # Check if the solution is correct
    is_correct = convolve_solver.is_solution(problem, solution)
    print(f"Is solution correct? {is_correct}")
