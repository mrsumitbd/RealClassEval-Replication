class FFTComplexScipyFFTpack:

    @staticmethod
    def _to_complex_array(data):
        import numpy as np

        if isinstance(data, dict):
            if "signal" in data:
                return FFTComplexScipyFFTpack._to_complex_array(data["signal"])
            if "x" in data:
                return FFTComplexScipyFFTpack._to_complex_array(data["x"])
            if "real" in data and "imag" in data:
                real = np.asarray(data["real"], dtype=float)
                imag = np.asarray(data["imag"], dtype=float)
                if real.shape != imag.shape:
                    raise ValueError("real and imag must have the same shape")
                return real + 1j * imag
            raise ValueError("Unsupported problem dictionary format")
        # list/array/tuple of either complex numbers or pairs [r, i]
        arr = np.asarray(data)
        if arr.dtype.kind == "c":
            return arr.astype(np.complex128)
        # If it is a 2D array with last dim 2 -> [real, imag] pairs
        if arr.ndim >= 1 and arr.shape[-1] == 2 and arr.dtype.kind in "fiu":
            real = arr[..., 0].astype(float)
            imag = arr[..., 1].astype(float)
            return (real + 1j * imag).reshape(-1)
        # Otherwise treat as real signal
        return arr.astype(float).astype(np.complex128)

    @staticmethod
    def _fft(x):
        try:
            from scipy import fftpack as _fftpack
            return _fftpack.fft(x)
        except Exception:
            import numpy as np
            return np.fft.fft(x)

    @staticmethod
    def _solution_to_complex_array(solution):
        import numpy as np
        if isinstance(solution, dict):
            if "fft" in solution:
                return FFTComplexScipyFFTpack._to_complex_array(solution["fft"])
            if "y" in solution:
                return FFTComplexScipyFFTpack._to_complex_array(solution["y"])
            if "real" in solution and "imag" in solution:
                real = np.asarray(solution["real"], dtype=float)
                imag = np.asarray(solution["imag"], dtype=float)
                if real.shape != imag.shape:
                    return None
                return real + 1j * imag
        # try as list/array of complex or [r,i] pairs
        try:
            return FFTComplexScipyFFTpack._to_complex_array(solution)
        except Exception:
            return None

    @staticmethod
    def _as_real_imag_dict(z):
        import numpy as np
        z = np.asarray(z, dtype=np.complex128)
        return {
            "real": (z.real).tolist(),
            "imag": (z.imag).tolist(),
        }

    @staticmethod
    def solve(problem):
        x = FFTComplexScipyFFTpack._to_complex_array(problem)
        y = FFTComplexScipyFFTpack._fft(x)
        return FFTComplexScipyFFTpack._as_real_imag_dict(y)

    @staticmethod
    def is_solution(problem, solution):
        import numpy as np
        atol = 1e-8
        rtol = 1e-12

        # compute expected
        try:
            x = FFTComplexScipyFFTpack._to_complex_array(problem)
            expected = FFTComplexScipyFFTpack._fft(x)
        except Exception:
            return False

        got = FFTComplexScipyFFTpack._solution_to_complex_array(solution)
        if got is None:
            return False

        expected = np.asarray(expected, dtype=np.complex128)
        got = np.asarray(got, dtype=np.complex128)

        if expected.shape != got.shape:
            return False

        return np.allclose(expected, got, rtol=rtol, atol=atol)
