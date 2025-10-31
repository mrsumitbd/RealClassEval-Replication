import numpy as np
import logging

class PSDConeProjection:
    """
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the PSDConeProjection."""
        pass

    def solve(self, problem):
        """
        Solve the psd_cone_projection problem.

        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection

        Returns:
            The solution in the format expected by the task
        """
        try:
            A = np.array(problem['A'])
            eigvals, eigvecs = np.linalg.eigh(A)
            np.maximum(eigvals, 0, out=eigvals)
            X = eigvecs * eigvals @ eigvecs.T
            return {'X': X}
        except Exception as e:
            logging.error(f'Error in solve method: {e}')
            raise e

    def is_solution(self, problem, solution):
        """
        Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        try:
            '\n            Check if the obtained solution is valid for the given problem.\n\n            Args:\n                problem: a dictionary of problem instance containing parameters.\n                solution: proposed solution to the problem.\n\n            Returns: a boolean indicating whether the given solution is actually the solution.\n            '
            if not all((key in solution for key in ['X'])):
                logging.error('Solution missing required keys.')
                return False
            reference_solution = self.solve(problem)
            reference_X = np.array(reference_solution['X'])
            A = np.array(problem['A'])
            proposed_X = np.array(solution['X'])
            if proposed_X.shape != reference_X.shape:
                logging.error('The solution has wrong dimension.')
                return False
            if not np.allclose(proposed_X, proposed_X.T, rtol=1e-05, atol=1e-08):
                logging.error('The solution is not symmetric')
                return False
            if not np.all(np.linalg.eigvals(proposed_X) >= -1e-05):
                logging.error('The solution is not positive semidefinite')
                return False
            objective_proposed = np.sum((A - proposed_X) ** 2)
            objective_reference = np.sum((A - reference_X) ** 2)
            if not np.isclose(objective_proposed, objective_reference, rtol=1e-05, atol=1e-08):
                logging.error(f'Proposed solution is not optimal. Proposed objective: {objective_proposed}, Reference objective: {objective_reference}')
                return False
            return True
        except Exception as e:
            logging.error(f'Error in is_solution method: {e}')
            return False