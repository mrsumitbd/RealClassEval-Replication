import numpy as np
import scipy.ndimage
import logging

class AffineTransform2D:
    """
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the AffineTransform2D."""
        self.order = 3
        self.mode = 'constant'

    def solve(self, problem):
        """
        Solve the affine_transform_2d problem.

        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d

        Returns:
            The solution in the format expected by the task
        """
        try:
            '\n            Solves the 2D affine transformation problem using scipy.ndimage.affine_transform.\n\n            :param problem: A dictionary representing the problem.\n            :return: A dictionary with key "transformed_image":\n                     "transformed_image": The transformed image as an array.\n            '
            image = problem['image']
            matrix = problem['matrix']
            try:
                transformed_image = scipy.ndimage.affine_transform(image, matrix, order=self.order, mode=self.mode)
            except Exception as e:
                logging.error(f'scipy.ndimage.affine_transform failed: {e}')
                return {'transformed_image': []}
            solution = {'transformed_image': transformed_image}
            return solution
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
            '\n            Check if the provided affine transformation solution is valid.\n\n            Checks structure, dimensions, finite values, and numerical closeness to\n            the reference scipy.ndimage.affine_transform output.\n\n            :param problem: The problem definition dictionary.\n            :param solution: The proposed solution dictionary.\n            :return: True if the solution is valid, False otherwise.\n            '
            if not all((k in problem for k in ['image', 'matrix'])):
                logging.error("Problem dictionary missing 'image' or 'matrix'.")
                return False
            image = problem['image']
            matrix = problem['matrix']
            if not isinstance(solution, dict) or 'transformed_image' not in solution:
                logging.error("Solution format invalid: missing 'transformed_image' key.")
                return False
            proposed_list = solution['transformed_image']
            if isinstance(proposed_list, np.ndarray):
                if proposed_list.size == 0:
                    proposed_list = []
                else:
                    proposed_list = proposed_list.tolist()
            if isinstance(proposed_list, np.ndarray):
                proposed_list = proposed_list.tolist()
            if isinstance(proposed_list, list) and proposed_list == [] or (isinstance(proposed_list, np.ndarray) and proposed_list.size == 0):
                logging.warning('Proposed solution is empty list (potential failure).')
                try:
                    ref_output = scipy.ndimage.affine_transform(image, matrix, order=self.order, mode=self.mode)
                    if ref_output.size == 0:
                        logging.info('Reference solver also produced empty result. Accepting empty solution.')
                        return True
                    else:
                        logging.error('Reference solver succeeded, but proposed solution was empty.')
                        return False
                except Exception:
                    logging.info('Reference solver also failed. Accepting empty solution.')
                    return True
            if not isinstance(proposed_list, (list, np.ndarray)):
                logging.error("'transformed_image' is not a list or array.")
                return False
            try:
                proposed_array = np.asarray(proposed_list, dtype=float)
            except ValueError:
                logging.error("Could not convert 'transformed_image' list to numpy float array.")
                return False
            if proposed_array.shape != image.shape:
                logging.error(f'Output shape {proposed_array.shape} != input shape {image.shape}.')
                return False
            if not np.all(np.isfinite(proposed_array)):
                logging.error("Proposed 'transformed_image' contains non-finite values.")
                return False
            try:
                ref_array = scipy.ndimage.affine_transform(image, matrix, order=self.order, mode=self.mode)
            except Exception as e:
                logging.error(f'Error computing reference solution: {e}')
                return False
            rtol = 1e-05
            atol = 1e-07
            is_close = np.allclose(proposed_array, ref_array, rtol=rtol, atol=atol)
            if not is_close:
                abs_diff = np.abs(proposed_array - ref_array)
                max_abs_err = np.max(abs_diff) if abs_diff.size > 0 else 0
                logging.error(f'Solution verification failed: Output mismatch. Max absolute error: {max_abs_err:.3f} (rtol={rtol}, atol={atol})')
                return False
            logging.debug('Solution verification successful.')
            return True
        except Exception as e:
            logging.error(f'Error in is_solution method: {e}')
            return False