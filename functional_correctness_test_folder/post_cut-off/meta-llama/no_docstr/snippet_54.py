
import numpy as np
from scipy import signal


class Convolve2DFullFill:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Convolve two 2D arrays using 'full' mode.

        Args:
        problem (dict): A dictionary containing 'array1' and 'array2' as keys.

        Returns:
        np.ndarray: The result of the 2D convolution.
        """
        array1 = problem['array1']
        array2 = problem['array2']
        return signal.convolve2d(array1, array2, mode='full')

    def is_solution(self, problem, solution):
        """
        Check if the given solution is correct.

        Args:
        problem (dict): A dictionary containing 'array1' and 'array2' as keys.
        solution (np.ndarray): The proposed solution.

        Returns:
        bool: True if the solution is correct, False otherwise.
        """
        expected_solution = self.solve(problem)
        return np.array_equal(solution, expected_solution)


# Example usage:
if __name__ == "__main__":
    convolve = Convolve2DFullFill()

    # Define the problem
    array1 = np.array([[1, 2], [3, 4]])
    array2 = np.array([[5, 6], [7, 8]])
    problem = {'array1': array1, 'array2': array2}

    # Solve the problem
    solution = convolve.solve(problem)
    print("Solution:")
    print(solution)

    # Check if the solution is correct
    is_correct = convolve.is_solution(problem, solution)
    print(f"Is solution correct? {is_correct}")
