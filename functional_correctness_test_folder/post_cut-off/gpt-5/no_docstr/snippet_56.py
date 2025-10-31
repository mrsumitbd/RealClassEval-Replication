import numpy as np


class FFTComplexScipyFFTpack:

    def __init__(self):
        self._use_scipy = False
        self._fft = None
        self._ifft = None
        try:
            from scipy import fftpack as _fftp
            self._fft = _fftp.fft
            self._ifft = _fftp.ifft
            self._use_scipy = True
        except Exception:
            # Fallback to numpy if scipy is not available
            self._fft = np.fft.fft
            self._ifft = np.fft.ifft

    def solve(self, problem):
        x, n, axis, norm, inverse = self._parse_problem(problem)
        if inverse:
            return self._ifft(x, n=n, axis=axis, norm=norm)
        return self._fft(x, n=n, axis=axis, norm=norm)

    def is_solution(self, problem, solution):
        x, n, axis, norm, inverse = self._parse_problem(problem)
        # Compare against NumPy reference
        if inverse:
            ref = np.fft.ifft(x, n=n, axis=axis, norm=norm)
        else:
            ref = np.fft.fft(x, n=n, axis=axis, norm=norm)
        if not self._allclose(solution, ref):
            return False
        # Round-trip consistency check
        if inverse:
            # If inverse was requested, forward of solution should match original x
            round_trip = np.fft.fft(solution, n=n, axis=axis, norm=norm)
            target = np.fft.fft(np.fft.ifft(
                x, n=n, axis=axis, norm=norm), n=n, axis=axis, norm=norm)
        else:
            round_trip = np.fft.ifft(solution, n=n, axis=axis, norm=norm)
            target = np.fft.ifft(np.fft.fft(
                x, n=n, axis=axis, norm=norm), n=n, axis=axis, norm=norm)
        return self._allclose(round_trip, target)

    def _parse_problem(self, problem):
        x = None
        n = None
        axis = -1
        norm = None
        inverse = False

        if isinstance(problem, dict):
            # Accept common keys
            if 'x' in problem:
                x = problem['x']
            elif 'signal' in problem:
                x = problem['signal']
            elif 'input' in problem:
                x = problem['input']
            elif 'data' in problem:
                x = problem['data']
            n = problem.get('n', None)
            axis = problem.get('axis', -1)
            norm = problem.get('norm', None)
            inverse = problem.get('inverse', False)
        elif isinstance(problem, (list, tuple)) and len(problem) > 0:
            x = problem[0]
            if len(problem) > 1 and problem[1] is not None:
                n = problem[1]
            if len(problem) > 2 and problem[2] is not None:
                axis = problem[2]
            if len(problem) > 3:
                norm = problem[3]
            if len(problem) > 4:
                inverse = bool(problem[4])
        else:
            x = problem

        if x is None:
            raise ValueError("No input array provided in problem.")
        x = np.asarray(x)
        return x, n, axis, norm, inverse

    def _allclose(self, a, b):
        # Use tolerances appropriate for FFT numerical noise
        return np.allclose(a, b, rtol=1e-6, atol=1e-8)
