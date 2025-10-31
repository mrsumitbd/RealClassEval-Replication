
import numpy as np


class Convolve2DFullFill:

    def __init__(self):
        pass

    def solve(self, problem):
        input_matrix, kernel = problem
        input_height, input_width = input_matrix.shape
        kernel_height, kernel_width = kernel.shape

        output_height = input_height + kernel_height - 1
        output_width = input_width + kernel_width - 1

        output = np.zeros((output_height, output_width))

        for i in range(output_height):
            for j in range(output_width):
                for m in range(kernel_height):
                    for n in range(kernel_width):
                        input_i = i - m
                        input_j = j - n
                        if 0 <= input_i < input_height and 0 <= input_j < input_width:
                            output[i, j] += input_matrix[input_i,
                                                         input_j] * kernel[m, n]

        return output

    def is_solution(self, problem, solution):
        input_matrix, kernel = problem
        expected_output = self.solve(problem)
        return np.array_equal(solution, expected_output)
