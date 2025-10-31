
class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.transformation_matrix = None

    def solve(self, problem):
        '''
        Solve the affine_transform_2d problem.
        Args:
            problem: Dictionary containing problem data specific to affine_transform_2d
        Returns:
            The solution in the format expected by the task
        '''
        # Extract source and target points from the problem
        source_points = problem.get('source_points', [])
        target_points = problem.get('target_points', [])

        # Check if we have enough points to solve the affine transformation
        if len(source_points) < 3 or len(target_points) < 3:
            raise ValueError(
                "At least 3 point pairs are required to solve the affine transformation.")

        # Convert points to numpy arrays for easier manipulation
        src = np.array(source_points, dtype=np.float32)
        dst = np.array(target_points, dtype=np.float32)

        # Calculate the affine transformation matrix
        self.transformation_matrix, _ = cv2.estimateAffine2D(src, dst)

        return {
            'transformation_matrix': self.transformation_matrix.tolist(),
            'source_points': source_points,
            'target_points': target_points
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Check if the solution contains the required keys
        if not all(key in solution for key in ['transformation_matrix', 'source_points', 'target_points']):
            return False

        # Check if the transformation matrix is valid
        if solution['transformation_matrix'] is None or len(solution['transformation_matrix']) != 2:
            return False

        # Check if the number of source and target points match
        if len(solution['source_points']) != len(solution['target_points']):
            return False

        # Check if the transformation matrix can transform source points to target points
        src = np.array(solution['source_points'], dtype=np.float32)
        dst = np.array(solution['target_points'], dtype=np.float32)
        transformed_src = cv2.transform(
            src.reshape(-1, 1, 2), np.array(solution['transformation_matrix'])).reshape(-1, 2)

        # Check if the transformed source points match the target points within a small tolerance
        if not np.allclose(transformed_src, dst, atol=1e-5):
            return False

        return True
