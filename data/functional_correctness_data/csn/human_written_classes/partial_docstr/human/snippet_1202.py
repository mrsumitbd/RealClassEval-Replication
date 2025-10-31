import numpy as np

class PinholeCamera:

    def __init__(self, matrix):
        self.matrix = np.reshape(matrix, (4, 4)).transpose()

    def screen_to_vector(self, move_vector):
        """Converts vector from the screen coordinates to the normalized vector in 3D."""
        move_vector[0] = -move_vector[0]
        res = np.append(np.array(move_vector), [0])
        res = self.inverse_matrix.dot(res)
        res /= np.linalg.norm(res)
        return res[0:3]

    @property
    def inverse_matrix(self):
        return np.linalg.inv(self.matrix)