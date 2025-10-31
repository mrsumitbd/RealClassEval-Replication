
import math
import cmath
from typing import List, Dict, Any


class FFTConvolution:
    '''
    Initial implementation of fft_convolution task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        pass

    def _next_power_of_two(self, n: int) -> int:
        """Return the next power of two greater than or equal to n."""
        return 1 << (n - 1).bit_length()

    def _fft(self, a: List[complex]) -> List[complex]:
        """Iterative Cooley–Tukey FFT (in-place)."""
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        length = 2
        while length <= n:
            ang = 2 * math.pi / length
            wlen = complex(math.cos(ang), math.sin(ang))
            for i in range(0, n, length):
                w = 1+0j
                for j in range(i, i + length // 2):
                    u = a[j]
                    v = a[j + length // 2] * w
                    a[j] = u + v
                    a[j + length // 2] = u - v
                    w *= wlen
            length <<= 1
        return a

    def _ifft(self, a: List[complex]) -> List[complex]:
        """Inverse FFT using conjugation trick."""
        n = len(a)
        a_conj = [x.conjugate() for x in a]
        self._fft(a_conj)
        return [x.conjugate() / n for x in a_conj]

    def solve(self, problem: Dict[str, Any]) -> List[float]:
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
                      Expected keys: 'a' and 'b', each a list of numbers.
        Returns:
            The convolution result as a list of floats.
        '''
        a = problem.get('a', [])
        b = problem.get('b', [])
        if not isinstance(a, list) or not isinstance(b, list):
            raise ValueError("Problem must contain lists 'a' and 'b'.")

        n = len(a) + len(b) - 1
        size = self._next_power_of_two(n)

        # Pad sequences
        fa = [complex(x, 0) for x in a] + [0] * (size - len(a))
        fb = [complex(x, 0) for x in b] + [0] * (size - len(b))

        # FFT
        self._fft(fa)
        self._fft(fb)

        # Pointwise multiplication
        for i in range(size):
            fa[i] *= fb[i]

        # Inverse FFT
        result_complex = self._ifft(fa)

        # Round small imaginary parts and truncate to required length
        result = [round(result_complex[i].real, 10) for i in range(n)]
        return result

    def is_solution(self, problem: Dict[str, Any], solution: List[float]) -> bool:
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Compute expected convolution naively
        a = problem.get('a', [])
        b = problem.get('b', [])
        if not isinstance(a, list) or not isinstance(b, list):
            return False
        n = len(a) + len(b) - 1
        expected = [0] * n
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                expected[i + j] += ai * bj

        # Compare with tolerance
        if len(solution) != n:
            return False
        for exp, sol in zip(expected, solution):
            if abs(exp - sol) > 1e-6:
                return False
        return True
