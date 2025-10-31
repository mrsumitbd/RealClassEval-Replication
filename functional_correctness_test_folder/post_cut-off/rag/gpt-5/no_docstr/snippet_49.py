import math
from typing import Any, Dict, Tuple, Optional

import numpy as np


class FFTComplexScipyFFTpack:
    '''
    Initial implementation of fft_cmplx_scipy_fftpack task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''
    @staticmethod
    def _import_fft_backend():
        try:
            from scipy import fftpack as sp_fft
            return "scipy.fftpack", sp_fft
        except Exception:
            # Fallback to numpy.fft
            return "numpy.fft", np.fft

    @staticmethod
    def _to_complex_array(x: Any) -> np.ndarray:
        # Accept dict with 'real'/'imag'
        if isinstance(x, dict) and "real" in x and "imag" in x:
            real = np.asarray(x["real"], dtype=float)
            imag = np.asarray(x["imag"], dtype=float)
            return real + 1j * imag

        # If numpy array with complex dtype already
        if isinstance(x, np.ndarray) and np.iscomplexobj(x):
            return x.astype(np.complex128, copy=False)

        # Convert lists or other arrays
        arr = np.asarray(x)
        if np.iscomplexobj(arr):
            return arr.astype(np.complex128, copy=False)

        # If representation is pairs on the last axis: [..., 2] -> complex
        if arr.ndim >= 1 and arr.shape[-1:] == (2,):
            real = arr[..., 0]
            imag = arr[..., 1]
            return real.astype(float) + 1j * imag.astype(float)

        # Real-only input
        return arr.astype(float) + 0j

    @staticmethod
    def _format_output(y: np.ndarray, libname: str, inverse: bool) -> Dict[str, Any]:
        return {
            "real": np.asanyarray(y.real).tolist(),
            "imag": np.asanyarray(y.imag).tolist(),
            "shape": list(y.shape),
            "ndim": int(y.ndim),
            "dtype": str(y.dtype),
            "library": libname,
            "inverse": bool(inverse),
        }

    @staticmethod
    def _get_input_from_problem(problem: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
        # Try to find the signal/data in a variety of commonly used keys
        for key in ("signal", "data", "x", "input", "array", "arr"):
            if key in problem:
                arr = FFTComplexScipyFFTpack._to_complex_array(problem[key])
                return arr, {"source_key": key}
        # If not found, raise a descriptive error
        raise KeyError(
            "No input array found in problem. Expected one of keys: signal, data, x, input, array, arr")

    @staticmethod
    def _effective_axes_and_shape(x: np.ndarray, problem: Dict[str, Any]) -> Tuple[Optional[Tuple[int, ...]], Optional[Tuple[int, ...]], Optional[int]]:
        # Determine axes for transform
        axes = problem.get("axes", None)
        axis = problem.get("axis", None)
        if axes is not None and axis is not None:
            # Prefer 'axes' if both given
            pass
        elif axis is not None:
            axes = (int(axis),)

        if axes is not None:
            axes = tuple(int(a) for a in axes)
            # Normalize negative axes
            axes = tuple(a if a >= 0 else a + x.ndim for a in axes)
        else:
            axes = None  # means all axes for n-d, or -1 for 1-d routines

        # Determine sizes
        s = problem.get("s", None)
        shape = problem.get("shape", None)
        n = problem.get("n", None)

        # Normalize sizes
        if shape is None and s is not None:
            if isinstance(s, int):
                shape = (int(s),)
            else:
                shape = tuple(int(v) for v in s)
        elif shape is not None:
            if isinstance(shape, int):
                shape = (int(shape),)
            else:
                shape = tuple(int(v) for v in shape)

        if n is not None:
            n = int(n)

        return axes, shape, n

    @staticmethod
    def _n_total_for_norm(x: np.ndarray, axes: Optional[Tuple[int, ...]], shape: Optional[Tuple[int, ...]], n_1d: Optional[int]) -> int:
        if x.ndim == 1:
            if n_1d is not None:
                return n_1d
            return x.shape[0]
        # n-dim
        if axes is None:
            axes = tuple(range(x.ndim))
        if shape is not None:
            # If provided, use provided sizes along transform axes
            if len(shape) == len(axes):
                sizes = shape
            else:
                # If shape provided without matching axes length, fallback to x sizes
                sizes = tuple(x.shape[a] for a in axes)
        else:
            sizes = tuple(x.shape[a] for a in axes)
        n_total = 1
        for v in sizes:
            n_total *= int(v)
        return n_total

    @staticmethod
    def _apply_norm_scaling(y: np.ndarray, norm: Optional[str], n_total: int, inverse: bool) -> np.ndarray:
        if not norm:
            return y
        if norm == "ortho":
            if inverse:
                # standard ifft scales 1/n; for ortho we want 1/sqrt(n):
                # multiply by sqrt(n) to go from 1/n to 1/sqrt(n)
                scale = math.sqrt(n_total)
                return y * scale
            else:
                # standard fft has scale 1; for ortho we want 1/sqrt(n)
                scale = 1.0 / math.sqrt(n_total)
                return y * scale
        # Unrecognized norm - ignore
        return y

    @staticmethod
    def _maybe_shift(y: np.ndarray, problem: Dict[str, Any]) -> np.ndarray:
        fftshift = bool(problem.get("fftshift", False)
                        or problem.get("shift", False))
        ifftshift = bool(problem.get("ifftshift", False))
        axes = problem.get("axes", None)
        axis = problem.get("axis", None)
        if axes is None and axis is not None:
            axes = (int(axis),)
        if axes is not None:
            axes = tuple(int(a) for a in axes)

        if fftshift:
            return np.fft.fftshift(y, axes=axes)
        if ifftshift:
            return np.fft.ifftshift(y, axes=axes)
        return y

    @staticmethod
    def solve(problem):
        '''
        Solve the fft_cmplx_scipy_fftpack problem.
        Args:
            problem: Dictionary containing problem data specific to fft_cmplx_scipy_fftpack
        Returns:
            The solution in the format expected by the task
        '''
        libname, fftmod = FFTComplexScipyFFTpack._import_fft_backend()
        x, _ = FFTComplexScipyFFTpack._get_input_from_problem(problem)

        inverse = bool(problem.get("inverse", False))
        norm = problem.get("norm", None)

        axes, shape, n_1d = FFTComplexScipyFFTpack._effective_axes_and_shape(
            x, problem)

        if x.ndim <= 1:
            # 1-D FFT along specified axis (default last)
            ax = -1 if axes is None else axes[0]
            if inverse:
                y = fftmod.ifft(x, n=n_1d, axis=ax)
            else:
                y = fftmod.fft(x, n=n_1d, axis=ax)
            n_total = FFTComplexScipyFFTpack._n_total_for_norm(
                x, (ax,), (n_1d,) if n_1d is not None else None, n_1d)
        else:
            # N-D FFT
            if inverse:
                y = fftmod.ifftn(x, shape=shape, axes=axes)
            else:
                y = fftmod.fftn(x, shape=shape, axes=axes)
            n_total = FFTComplexScipyFFTpack._n_total_for_norm(
                x, axes, shape, None)

        y = FFTComplexScipyFFTpack._apply_norm_scaling(
            y, norm, n_total, inverse)
        y = FFTComplexScipyFFTpack._maybe_shift(y, problem)

        return FFTComplexScipyFFTpack._format_output(y, libname, inverse)

    @staticmethod
    def _extract_complex_from_solution(solution: Any) -> np.ndarray:
        if isinstance(solution, dict) and "real" in solution and "imag" in solution:
            return FFTComplexScipyFFTpack._to_complex_array({"real": solution["real"], "imag": solution["imag"]})
        return FFTComplexScipyFFTpack._to_complex_array(solution)

    @staticmethod
    def _expected_from_problem(problem: Dict[str, Any]) -> Optional[np.ndarray]:
        for key in ("expected", "target", "y", "fft", "output"):
            if key in problem:
                try:
                    return FFTComplexScipyFFTpack._to_complex_array(problem[key])
                except Exception:
                    # If it's a dict formatted like solve's output, try real/imag inside
                    val = problem[key]
                    if isinstance(val, dict) and "real" in val and "imag" in val:
                        return FFTComplexScipyFFTpack._to_complex_array(val)
        return None

    @staticmethod
    def is_solution(problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        atol = float(problem.get("atol", 1e-6))
        rtol = float(problem.get("rtol", 1e-7))

        # Convert proposed solution to a complex ndarray
        try:
            sol_arr = FFTComplexScipyFFTpack._extract_complex_from_solution(
                solution)
        except Exception:
            return False

        # If explicit expected present in the problem, compare against that
        expected = FFTComplexScipyFFTpack._expected_from_problem(problem)
        if expected is not None:
            try:
                return np.allclose(sol_arr, expected, atol=atol, rtol=rtol, equal_nan=True)
            except Exception:
                return False

        # Otherwise compute a reference via our solver and compare
        try:
            ref = FFTComplexScipyFFTpack.solve(problem)
            ref_arr = FFTComplexScipyFFTpack._to_complex_array(ref)
            if ref_arr.size == 0 and sol_arr.size == 0:
                return True
            return np.allclose(sol_arr, ref_arr, atol=atol, rtol=rtol, equal_nan=True)
        except Exception:
            # As a fallback validation, check transform-inverse consistency
            try:
                x, _ = FFTComplexScipyFFTpack._get_input_from_problem(problem)
                libname, fftmod = FFTComplexScipyFFTpack._import_fft_backend()
                inverse = bool(problem.get("inverse", False))
                axes, shape, n_1d = FFTComplexScipyFFTpack._effective_axes_and_shape(
                    x, problem)
                norm = problem.get("norm", None)
                # Build inverse/forward to check round-trip consistency
                if inverse:
                    # Provided solution is inverse FFT(x) -> apply forward FFT to compare to x
                    if sol_arr.ndim <= 1:
                        ax = -1 if axes is None else axes[0]
                        y = fftmod.fft(sol_arr, n=n_1d, axis=ax)
                    else:
                        y = fftmod.fftn(sol_arr, shape=shape, axes=axes)
                    # undo any norm scaling used during solve
                    n_total = FFTComplexScipyFFTpack._n_total_for_norm(
                        sol_arr, axes if sol_arr.ndim > 1 else (ax,), shape, n_1d if sol_arr.ndim <= 1 else None)
                    if norm == "ortho":
                        # Forward scaling for ortho was 1/sqrt(n), so undo:
                        y = y * math.sqrt(n_total)
                    return np.allclose(y, x, atol=atol, rtol=rtol, equal_nan=True)
                else:
                    # Provided solution is forward FFT(x) -> apply inverse FFT to compare to x
                    if sol_arr.ndim <= 1:
                        ax = -1 if axes is None else axes[0]
                        y = fftmod.ifft(sol_arr, n=n_1d, axis=ax)
                    else:
                        y = fftmod.ifftn(sol_arr, shape=shape, axes=axes)
                    n_total = FFTComplexScipyFFTpack._n_total_for_norm(
                        sol_arr, axes if sol_arr.ndim > 1 else (ax,), shape, n_1d if sol_arr.ndim <= 1 else None)
                    if norm == "ortho":
                        # Inverse scaling for ortho was multiply by sqrt(n) after standard ifft
                        y = y / math.sqrt(n_total)
                    return np.allclose(y, x, atol=atol, rtol=rtol, equal_nan=True)
            except Exception:
                return False
