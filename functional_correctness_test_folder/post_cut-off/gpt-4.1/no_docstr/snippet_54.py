
import numpy as np


class Convolve2DFullFill:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        problem: dict with keys 'input', 'kernel'
        Returns: 2D list, the full convolution of input and kernel
        """
        input_arr = np.array(problem['input'])
        kernel = np.array(problem['kernel'])
        # Flip the kernel for convolution
        kernel = np.flipud(np.fliplr(kernel))
        # Get shapes
        in_h, in_w = input_arr.shape
        k_h, k_w = kernel.shape
        # Output shape for 'full' convolution
        out_h = in_h + k_h - 1
        out_w = in_w + k_w - 1
        # Pad input
        pad_h = k_h - 1
        pad_w = k_w - 1
        padded = np.pad(input_arr, ((pad_h, pad_h), (pad_w, pad_w)),
                        mode='constant', constant_values=0)
        # Output array
        output = np.zeros((out_h, out_w), dtype=int)
        # Perform convolution
        for i in range(out_h):
            for j in range(out_w):
                region = padded[i:i+k_h, j:j+k_w]
                output[i, j] = np.sum(region * kernel)
        return output.tolist()

    def is_solution(self, problem, solution):
        expected = self.solve(problem)
        return expected == solution
