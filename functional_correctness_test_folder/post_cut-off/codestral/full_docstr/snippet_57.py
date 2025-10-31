
import numpy as np


class FFTConvolution:

    def __init__(self):
        pass

    def solve(self, problem):
        signal1 = problem['signal1']
        signal2 = problem['signal2']
        result = np.convolve(signal1, signal2, mode='full')
        return {'result': result}

    def is_solution(self, problem, solution):
        signal1 = problem['signal1']
        signal2 = problem['signal2']
        expected_result = np.convolve(signal1, signal2, mode='full')
        return np.array_equal(solution['result'], expected_result)
