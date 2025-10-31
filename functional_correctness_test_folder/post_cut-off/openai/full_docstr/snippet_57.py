
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
        # Try to import numpy for efficient FFT; fall back to pure Python if unavailable
        try:
            import numpy as np
            self._np = np
            self._use_numpy = True
        except Exception:
            self._np = None
            self._use_numpy = False

    def _next_power_of_two(self, n: int) -> int:
        """Return the next power of two >= n."""
        return 1 << (n - 1).bit_length()

    def _fft(self, a: List[complex]) -> List[complex]:
        """Compute FFT of a list using numpy if available, else recursive Cooley–Tukey."""
        if self._use_numpy:
            return list(self._np.fft.fft(a))
        # Recursive FFT (Cooley–Tukey) for power-of-two length
        n = len(a)
        if n == 1:
            return a
        even = self._fft(a[0::2])
        odd = self._fft(a[1::2])
        T = [cmath.exp(-2j * math.pi * k / n) * odd[k] for k in range(n // 2)]
        return [even[k] + T[k] for k in range(n // 2)] + \
               [even[k] - T[k] for k in range(n // 2)]

    def _ifft(self, a: List[complex]) -> List[complex]:
        """Compute inverse FFT."""
        if self._use_numpy:
            return list(self._np.fft.ifft(a))
        # Inverse FFT via conjugation
        conj = [x.conjugate() for x in a]
        y = self._fft(conj)
        return [x.conjugate() / len(a) for x in y]

    def solve(self, problem: Dict[str, Any]) -> List[float]:
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
                      Expected keys: 'a' and 'b', each a list of real numbers.
        Returns:
            The convolution of a and b as a list of floats.
        '''
        a = problem.get('a', [])
        b = problem.get('b', [])
        if not isinstance(a, list) or not isinstance(b, list):
            raise ValueError("Problem must contain lists 'a' and 'b'.")

        n = len(a) + len(b) - 1
        size = self._next_power_of_two(n)

        # Pad sequences
        a_pad = [complex(x) for x in a] + [0] * (size - len(a))
        b_pad = [complex(x) for x in b] + [0] * (size - len(b))

        # FFT
        A = self._fft(a_pad)
        B = self._fft(b_pad)

        # Pointwise multiplication
        C = [A[i] * B[i] for i in range(size)]

        # Inverse FFT
        c = self._ifft(C)

        # Truncate to actual convolution length and take real part
        result = [c[i].real for i in range(n)]
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
        expected = [0.0] * n
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                expected[i + j] += ai * bj

        if not isinstance(solution, list) or len(solution) != n:
            return False

        # Compare with tolerance
        eps = 1e-6
        for exp_val, sol_val in zip(expected, solution):
            if abs(exp_val - sol_val) > eps:
                return False
        return True
