
class AffineTransform2D:
    '''
    Initial implementation of affine_transform_2d task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the AffineTransform2D.'''
        self.matrix = None
        self.translation = None

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

        if len(source_points) != len(target_points) or len(source_points) < 3:
            raise ValueError(
                "Invalid number of points. Need at least 3 pairs of points.")

        # Convert points to numpy arrays for easier manipulation
        src = np.array(source_points)
        tgt = np.array(target_points)

        # Calculate centroids
        src_centroid = np.mean(src, axis=0)
        tgt_centroid = np.mean(tgt, axis=0)

        # Center the points
        src_centered = src - src_centroid
        tgt_centered = tgt - tgt_centroid

        # Calculate the covariance matrix
        H = np.dot(src_centered.T, tgt_centered)

        # Singular Value Decomposition
        U, S, Vt = np.linalg.svd(H)

        # Calculate rotation matrix
        R = np.dot(Vt.T, U.T)

        # Special reflection case
        if np.linalg.det(R) < 0:
            Vt[-1, :] *= -1
            R = np.dot(Vt.T, U.T)

        # Calculate translation
        self.translation = tgt_centroid - np.dot(R, src_centroid)

        # Store the rotation matrix
        self.matrix = R

        return {
            'rotation_matrix': R.tolist(),
            'translation_vector': self.translation.tolist()
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
        if not isinstance(solution, dict):
            return False

        rotation_matrix = solution.get('rotation_matrix')
        translation_vector = solution.get('translation_vector')

        if rotation_matrix is None or translation_vector is None:
            return False

        try:
            rotation_matrix = np.array(rotation_matrix)
            translation_vector = np.array(translation_vector)
        except (ValueError, TypeError):
            return False

        # Check if rotation matrix is 2x2 and orthogonal
        if rotation_matrix.shape != (2, 2):
            return False

        if not np.allclose(np.dot(rotation_matrix.T, rotation_matrix), np.eye(2)):
            return False

        # Check if translation vector is 1D with length 2
        if translation_vector.shape != (2,):
            return False

        # Verify the solution by applying it to source points and comparing with target points
        source_points = problem.get('source_points', [])
        target_points = problem.get('target_points', [])

        if len(source_points) != len(target_points):
            return False

        src = np.array(source_points)
        tgt = np.array(target_points)

        transformed_points = np.dot(
            src, rotation_matrix.T) + translation_vector

        return np.allclose(transformed_points, tgt, atol=1e-6)
