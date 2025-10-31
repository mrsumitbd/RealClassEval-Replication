
import math
import cmath


class FFTConvolution:
    def __init__(self):
        pass

    def _next_power_of_two(self, n):
        return 1 << (n - 1).bit_length()

    def _fft(self, a, invert=False):
        n = len(a)
        if n == 1:
            return a
        a0 = self._fft(a[0::2], invert)
        a1 = self._fft(a[1::2], invert)
        ang = 2 * math.pi / n * (-1 if invert else 1)
        w = 1
        wn = cmath.rect(1, ang)
        res = [0] * n
        for i in range(n // 2):
            u = a0[i]
            v = a1[i] * w
            res[i] = u + v
            res[i + n // 2] = u - v
            w *= wn
        return res

    def _convolve(self, a, b):
        n = len(a) + len(b) - 1
        size = self._next_power_of_two(n)
        fa = [complex(x, 0) for x in a] + [0] * (size - len(a))
        fb = [complex(x, 0) for x in b] + [0] * (size - len(b))
        fa = self._fft(fa)
        fb = self._fft(fb)
        for i in range(size):
            fa[i] *= fb[i]
        fa = self._fft(fa, invert=True)
        result = [int(round(fa[i].real / size)) for i in range(n)]
        return result

    def solve(self, problem):
        """
        Expects problem to be a dict with keys 'a' and 'b' containing lists of numbers.
        Returns the convolution of a and b as a list of integers.
        """
        a = problem.get('a', [])
        b = problem.get('b', [])
        return self._convolve(a, b)

    def is_solution(self, problem, solution):
        """
        Checks whether the provided solution matches the expected convolution.
        The problem dict may contain an 'expected' key with the correct result.
        If 'expected' is not provided, the method returns False.
        """
        expected = problem.get('expected')
        if expected is None:
            return False
        return solution == expected
