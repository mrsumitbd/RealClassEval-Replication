
import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        matrix = np.array(problem['matrix'])
        n = matrix.shape[0]

        lower = np.eye(n)
        upper = np.copy(matrix)

        for i in range(n):
            for j in range(i+1, n):
                factor = upper[j, i] / upper[i, i]
                lower[j, i] = factor
                upper[j] = upper[j] - factor * upper[i]

        solution = {
            'lower': lower.tolist(),
            'upper': upper.tolist()
        }
        return solution

    def is_solution(self, problem, solution):
        matrix = np.array(problem['matrix'])
        lower = np.array(solution['lower'])
        upper = np.array(solution['upper'])

        product = np.dot(lower, upper)
        return np.allclose(product, matrix)
