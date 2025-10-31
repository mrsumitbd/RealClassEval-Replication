class FFTConvolution:

    def __init__(self):
        '''Initialize the FFTConvolution.'''
        pass

    def solve(self, problem):
        '''
        Solve the fft_convolution problem.
        Args:
            problem: Dictionary containing problem data specific to fft_convolution
        Returns:
            The solution in the format expected by the task
        '''
        a, b = self._extract_sequences(problem)
        mode = problem.get('mode', 'full')  # 'full', 'same', 'valid'
        circular = problem.get('circular', False)
        n_circ = problem.get('n', None)
        return_int = problem.get('return_int', None)
        tol = problem.get('tol', 1e-9)

        if return_int is None:
            return_int = all(self._is_int_like_list(x) for x in (a, b))

        if circular:
            if n_circ is None:
                n_circ = max(len(a), len(b))
            a = self._wrap_to_length(a, n_circ)
            b = self._wrap_to_length(b, n_circ)
            nfft = self._next_pow2(n_circ)
            fa = self._fft(self._pad_complex(a, nfft))
            fb = self._fft(self._pad_complex(b, nfft))
            fc = [fa[i] * fb[i] for i in range(nfft)]
            c = self._ifft(fc)
            c = [c[i].real for i in range(n_circ)]
        else:
            full_len = len(a) + len(b) - 1
            nfft = self._next_pow2(full_len)
            fa = self._fft(self._pad_complex(a, nfft))
            fb = self._fft(self._pad_complex(b, nfft))
            fc = [fa[i] * fb[i] for i in range(nfft)]
            c_full = self._ifft(fc)
            c_full = [c_full[i].real for i in range(full_len)]
            if mode == 'full':
                c = c_full
            elif mode == 'same':
                L = max(len(a), len(b))
                start = (full_len - L) // 2
                c = c_full[start:start + L]
            elif mode == 'valid':
                L = abs(len(a) - len(b)) + 1
                start = min(len(a), len(b)) - 1
                c = c_full[start:start + L]
            else:
                raise ValueError(
                    "Invalid mode. Use 'full', 'same', or 'valid'.")

        c = [0.0 if abs(x) < tol else x for x in c]
        if return_int:
            c = [int(round(x)) for x in c]
        return c

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            comp = self.solve(problem)
        except Exception:
            return False

        if not isinstance(solution, list):
            return False
        if len(solution) != len(comp):
            return False

        tol = problem.get('check_tol', 1e-6)
        # Allow integer exact match or float within tolerance
        for s, c in zip(solution, comp):
            if isinstance(c, int) and isinstance(s, int):
                if s != c:
                    return False
            else:
                try:
                    sv = float(s)
                    cv = float(c)
                except Exception:
                    return False
                if abs(sv - cv) > tol:
                    return False
        return True

    # Helpers

    def _extract_sequences(self, problem):
        keys = [
            ('a', 'b'),
            ('x', 'h'),
            ('signal', 'kernel'),
            ('u', 'v'),
        ]
        for k1, k2 in keys:
            if k1 in problem and k2 in problem:
                a = problem[k1]
                b = problem[k2]
                break
        else:
            raise ValueError(
                "Problem must contain two sequences, e.g., ('a','b') or ('signal','kernel').")

        a = list(a)
        b = list(b)
        if not all(isinstance(v, (int, float)) for v in a + b):
            raise ValueError("Sequences must contain numbers.")
        return a, b

    def _is_int_like_list(self, arr):
        return all(isinstance(v, int) or (isinstance(v, float) and v.is_integer()) for v in arr)

    def _next_pow2(self, n):
        if n <= 1:
            return 1
        p = 1
        while p < n:
            p <<= 1
        return p

    def _pad_complex(self, seq, n):
        out = [0j] * n
        m = min(len(seq), n)
        for i in range(m):
            out[i] = complex(seq[i], 0.0)
        return out

    def _fft(self, a):
        import math
        n = len(a)
        j = 0
        A = list(a)
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                A[i], A[j] = A[j], A[i]
        length = 2
        while length <= n:
            ang = -2 * math.pi / length
            wlen = complex(math.cos(ang), math.sin(ang))
            for i in range(0, n, length):
                w = 1 + 0j
                half = length // 2
                for k in range(half):
                    u = A[i + k]
                    v = A[i + k + half] * w
                    A[i + k] = u + v
                    A[i + k + half] = u - v
                    w *= wlen
            length <<= 1
        return A

    def _ifft(self, A):
        n = len(A)
        conj = [x.conjugate() for x in A]
        y = self._fft(conj)
        return [(v.conjugate() / n) for v in y]

    def _wrap_to_length(self, seq, n):
        out = [0.0] * n
        if n <= 0:
            return []
        for i, v in enumerate(seq):
            out[i % n] += v
        return out
