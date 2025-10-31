
import numpy as np


class Convolve2DFullFill:

    def __init__(self):

        pass

    def solve(self, problem):

        image = problem['image']
        kernel = problem['kernel']
        solution = np.zeros(
            (image.shape[0] + kernel.shape[0] - 1, image.shape[1] + kernel.shape[1] - 1))
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                solution[i:i+kernel.shape[0], j:j +
                         kernel.shape[1]] += image[i, j] * kernel
        return solution

    def is_solution(self, problem, solution):

        image = problem['image']
        kernel = problem['kernel']
        expected_solution = np.zeros(
            (image.shape[0] + kernel.shape[0] - 1, image.shape[1] + kernel.shape[1] - 1))
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                expected_solution[i:i+kernel.shape[0], j:j +
                                  kernel.shape[1]] += image[i, j] * kernel
        return np.allclose(solution, expected_solution)
