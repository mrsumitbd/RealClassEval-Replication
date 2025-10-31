
class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        self.tolerance = 1e-6

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        import numpy as np
        from scipy.optimize import minimize

        # Extract data from problem
        A = problem.get('A', np.array([]))
        b = problem.get('b', np.array([]))
        C = problem.get('C', np.array([]))
        d = problem.get('d', np.array([]))

        # Objective function: minimize 0.5 * x^T * C * x + d^T * x
        def objective(x):
            return 0.5 * np.dot(x.T, np.dot(C, x)) + np.dot(d.T, x)

        # Constraint function: A * x = b
        def constraint(x):
            return np.dot(A, x) - b

        # Initial guess
        x0 = np.zeros(C.shape[1])

        # Define constraints in the form required by scipy.optimize.minimize
        cons = {'type': 'eq', 'fun': constraint}

        # Perform optimization
        result = minimize(objective, x0, constraints=cons)

        # Return the solution
        return result.x

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        import numpy as np

        # Extract data from problem
        A = problem.get('A', np.array([]))
        b = problem.get('b', np.array([]))
        C = problem.get('C', np.array([]))

        # Check if A * solution = b within tolerance
        if not np.allclose(np.dot(A, solution), b, atol=self.tolerance):
            return False

        # Check if C * solution is positive semi-definite
        if not np.all(np.linalg.eigvals(np.dot(solution.T, np.dot(C, solution))) >= -self.tolerance):
            return False

        return True
