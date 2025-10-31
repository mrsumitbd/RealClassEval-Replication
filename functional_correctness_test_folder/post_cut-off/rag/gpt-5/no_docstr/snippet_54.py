import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


Number = Union[int, float]
Grid = List[List[Number]]


class Convolve2DFullFill:
    '''
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the Convolve2DFullFill.'''
        pass

    def _is_rectangular(self, grid: Grid) -> bool:
        if not isinstance(grid, list) or not grid:
            return False
        if not all(isinstance(row, list) for row in grid):
            return False
        width = len(grid[0])
        if width == 0:
            return False
        return all(len(row) == width for row in grid)

    def _grid_shape(self, grid: Grid) -> Tuple[int, int]:
        return (len(grid), len(grid[0]) if grid else 0)

    def _has_float(self, grid: Grid) -> bool:
        for row in grid:
            for v in row:
                if isinstance(v, float) and not v.is_integer():
                    return True
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    # floats that are integer valued count as int-like
                    if isinstance(v, float) and v.is_integer():
                        continue
                else:
                    # non-number types
                    return True
        return False

    def _to_number(self, v: Any) -> Number:
        if isinstance(v, bool):
            return int(v)
        if isinstance(v, (int, float)):
            return v
        # Attempt coercion
        try:
            if '.' in str(v):
                return float(v)
            return int(v)
        except Exception:
            raise TypeError(f"Grid value {v!r} is not numeric")

    def _flip_kernel(self, kernel: Grid) -> Grid:
        return [row[::-1] for row in kernel[::-1]]

    def _convolve2d_full(self, image: Grid, kernel: Grid, fill_value: Number = 0) -> Grid:
        if not self._is_rectangular(image):
            raise ValueError("Image must be a non-empty rectangular grid")
        if not self._is_rectangular(kernel):
            raise ValueError("Kernel must be a non-empty rectangular grid")

        H, W = self._grid_shape(image)
        kH, kW = self._grid_shape(kernel)

        # Ensure numeric types
        img: List[List[Number]] = [
            [self._to_number(v) for v in row] for row in image]
        ker: List[List[Number]] = [
            [self._to_number(v) for v in row] for row in kernel]
        fill_value = self._to_number(fill_value)

        # Flip kernel for convolution
        ker_f = self._flip_kernel(ker)

        out_h = H + kH - 1
        out_w = W + kW - 1

        use_float = (
            any(isinstance(v, float) and not float(v).is_integer()
                for row in img for v in row)
            or any(isinstance(v, float) and not float(v).is_integer() for row in ker for v in row)
            or isinstance(fill_value, float)
        )

        def get_img(ii: int, jj: int) -> Number:
            if 0 <= ii < H and 0 <= jj < W:
                return img[ii][jj]
            return fill_value

        out: Grid = []
        base_i = kH - 1
        base_j = kW - 1

        for oi in range(out_h):
            row_out: List[Number] = []
            for oj in range(out_w):
                acc: float = 0.0
                for ki in range(kH):
                    ii = oi - base_i + ki
                    for kj in range(kW):
                        jj = oj - base_j + kj
                        acc += float(ker_f[ki][kj]) * float(get_img(ii, jj))
                if not use_float:
                    # Round to nearest int safely if values are integer-valued
                    val = int(round(acc))
                else:
                    val = acc
                row_out.append(val)
            out.append(row_out)
        return out

    def _extract_single_case(self, case: Dict[str, Any]) -> Optional[Grid]:
        for key in ("image", "input", "grid"):
            if key in case:
                return case[key]
        return None

    def _extract_kernel(self, problem: Dict[str, Any], fallback: Optional[Dict[str, Any]] = None) -> Optional[Grid]:
        if "kernel" in problem:
            return problem["kernel"]
        if fallback is not None and "kernel" in fallback:
            return fallback["kernel"]
        return None

    def solve(self, problem):
        '''
        Solve the convolve2d_full_fill problem.
        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill
        Returns:
            The solution in the format expected by the task
        '''
        if not isinstance(problem, dict):
            raise TypeError("Problem must be a dictionary")

        fill_value = problem.get("fill_value", 0)

        # Direct single-case solve
        single_image = self._extract_single_case(problem)
        kernel = self._extract_kernel(problem)
        if single_image is not None and kernel is not None:
            return self._convolve2d_full(single_image, kernel, fill_value)

        # Train/Test style
        if "train" in problem:
            train: Sequence[Dict[str, Any]] = problem["train"]
            if not isinstance(train, Sequence) or not train:
                raise ValueError(
                    "Problem 'train' must be a non-empty list of cases")

            # Try to get kernel from problem or the first training pair
            kernel = self._extract_kernel(problem, train[0])
            if kernel is None:
                raise ValueError(
                    "Kernel not provided in problem or training examples")

            # Optionally validate training consistency if outputs provided
            for pair in train:
                inp = self._extract_single_case(pair) or pair.get("input")
                if inp is None:
                    continue
                pred = self._convolve2d_full(inp, kernel, fill_value)
                if "output" in pair and self._is_rectangular(pair["output"]) and self._is_rectangular(pred):
                    # basic equality check
                    if not self._grids_equal(pair["output"], pred):
                        # Proceed anyway; initial implementation does not learn kernels
                        pass

            # Solve tests
            if "test" in problem:
                test_cases: Sequence[Dict[str, Any]] = problem["test"]
                results: List[Grid] = []
                for case in test_cases:
                    inp = self._extract_single_case(case)
                    if inp is None:
                        raise ValueError(
                            "Each test case must contain an input grid")
                    results.append(self._convolve2d_full(
                        inp, kernel, fill_value))
                return results

            # If no test, try to solve for a single provided input
            if single_image is not None:
                return self._convolve2d_full(single_image, kernel, fill_value)

        raise ValueError("Unsupported problem format for convolve2d_full_fill")

    def _grids_equal(self, a: Grid, b: Grid, tol: float = 1e-9) -> bool:
        if not self._is_rectangular(a) or not self._is_rectangular(b):
            return False
        if self._grid_shape(a) != self._grid_shape(b):
            return False
        for i in range(len(a)):
            for j in range(len(a[0])):
                va = self._to_number(a[i][j])
                vb = self._to_number(b[i][j])
                if isinstance(va, float) or isinstance(vb, float):
                    if not math.isfinite(float(va)) or not math.isfinite(float(vb)):
                        if va != vb:
                            return False
                    elif abs(float(va) - float(vb)) > tol:
                        return False
                else:
                    if int(va) != int(vb):
                        return False
        return True

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # If expected outputs are provided, verify strictly
        expected = None
        if isinstance(problem, dict):
            if "expected" in problem:
                expected = problem["expected"]
            elif "output" in problem:
                expected = problem["output"]
            elif "test" in problem and all(isinstance(t, dict) and "output" in t for t in problem["test"]):
                expected = [t["output"] for t in problem["test"]]

        if expected is not None:
            # Compare solution with expected
            if isinstance(expected, list) and expected and isinstance(expected[0], list) and expected and isinstance(expected[0], list) and expected and expected and isinstance(expected[0][0], (int, float)):
                # single grid expected
                if not isinstance(solution, list):
                    return False
                return self._grids_equal(expected, solution)
            else:
                # possibly list of grids
                if not isinstance(solution, list) or not isinstance(expected, list) or len(solution) != len(expected):
                    return False
                for s, e in zip(solution, expected):
                    if not self._grids_equal(e, s):
                        return False
                return True

        # Without explicit expected, perform format validation
        def is_grid(x: Any) -> bool:
            return isinstance(x, list) and len(x) > 0 and all(isinstance(r, list) and len(r) > 0 for r in x)

        if "test" in problem:
            # Expect list of grids
            if not isinstance(solution, list) or len(solution) != len(problem["test"]):
                return False
            if not all(is_grid(g) for g in solution):
                return False
            return True

        # Single-case solution should be a grid
        return is_grid(solution)
