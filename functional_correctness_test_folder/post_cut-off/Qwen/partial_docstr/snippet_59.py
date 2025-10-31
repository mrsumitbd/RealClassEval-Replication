
import numpy as np
from scipy.optimize import minimize


class PSDConeProjection:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        # Extracting necessary data from the problem dictionary
        A = problem.get('A', np.array([]))
        b = problem.get('b', np.array([]))
        C = problem.get('C', np.array([]))
        d = problem.get('d', np.array([]))
        # Default to identity matrix if not provided
        X0 = problem.get('X0', np.eye(A.shape[1]))

        # Objective function: minimize 0.5 * tr(C * X) + d^T * x
        def objective(X_flat):
            X = X_flat.reshape((A.shape[1], A.shape[1]))
            return 0.5 * np.trace(C @ X) + d @ X.flatten()

        # Constraint function: A * vec(X) = b
        def constraint(X_flat):
            X = X_flat.reshape((A.shape[1], A.shape[1]))
            return A @ X.flatten() - b

        # PSD constraint: X must be positive semidefinite
        def psd_constraint(X_flat):
            X = X_flat.reshape((A.shape[1], A.shape[1]))
            return np.linalg.eigvalsh(X)  # Eigenvalues must be non-negative

        # Initial guess
        X0_flat = X0.flatten()

        # Constraints dictionary
        cons = [{'type': 'eq', 'fun': constraint},
                {'type': 'ineq', 'fun': psd_constraint}]

        # Bounds for the variables (none for PSD matrices)
        bounds = [(None, None)] * X0_flat.size

        # Optimization
        result = minimize(objective, X0_flat, method='SLSQP',
                          bounds=bounds, constraints=cons)

        # Reshape the solution back to matrix form
        X_sol = result.x.reshape((A.shape[1], A.shape[1]))

        return X_sol

    def is_solution(self, problem, solution):
        # Extracting necessary data from the problem dictionary
        A = problem.get('A', np.array([]))
        b = problem.get('b', np.array([]))
        C = problem.get('C', np.array([]))
        d = problem.get('d', np.array([]))

        # Check if A * vec(solution) = b
        if not np.allclose(A @ solution.flatten(), b):
            return False

        # Check if solution is positive semidefinite
        if not np.all(np.linalg.eigvalsh(solution) >= 0):
            return False

        return True
