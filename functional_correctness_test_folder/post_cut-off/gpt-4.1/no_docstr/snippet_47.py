
import numpy as np


class Convolve2DFullFill:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        problem: dict with keys 'matrix' and 'kernel'
        Returns the full 2D convolution result as a list of lists.
        """
        matrix = np.array(problem['matrix'])
        kernel = np.array(problem['kernel'])
        m, n = matrix.shape
        km, kn = kernel.shape

        # Flip the kernel for convolution
        kernel_flipped = np.flipud(np.fliplr(kernel))

        # Output size for 'full' convolution
        out_shape = (m + km - 1, n + kn - 1)
        output = np.zeros(out_shape, dtype=matrix.dtype)

        # Pad the input matrix
        pad_height = km - 1
        pad_width = kn - 1
        padded_matrix = np.pad(matrix, ((pad_height, pad_height),
                               (pad_width, pad_width)), mode='constant', constant_values=0)

        # Perform convolution
        for i in range(out_shape[0]):
            for j in range(out_shape[1]):
                region = padded_matrix[i:i+km, j:j+kn]
                output[i, j] = np.sum(region * kernel_flipped)

        return output.tolist()

    def is_solution(self, problem, solution):
        expected = self.solve(problem)
        # Compare as lists of lists
        if len(expected) != len(solution):
            return False
        for row1, row2 in zip(expected, solution):
            if len(row1) != len(row2):
                return False
            for a, b in zip(row1, row2):
                if isinstance(a, float) or isinstance(b, float):
                    if not np.isclose(a, b):
                        return False
                else:
                    if a != b:
                        return False
        return True
