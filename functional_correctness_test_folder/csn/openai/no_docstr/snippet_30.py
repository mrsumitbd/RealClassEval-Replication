
import concurrent.futures
import threading
import traceback
from typing import Any, Callable, Iterable, List, Optional, Union


class LazyOpResult:
    """
    A lightweight container that defers the evaluation of an expression until
    :meth:`evaluate` is called. The expression can be a Python callable or a
    string that will be evaluated with :func:`eval`. Optional transformation
    passes can be applied to the result. The class is intentionally simple
    and does not depend on external libraries.
    """

    def __init__(
        self,
        expr: Union[Callable[..., Any], str],
        weld_type: str,
        dim: int,
    ) -> None:
        """
        Parameters
        ----------
        expr
            The expression to evaluate lazily. It can be a callable or a string.
        weld_type
            A string describing the type of operation (used only for
            informational purposes).
        dim
            An integer dimension value (used only for informational purposes).
        """
        self.expr = expr
        self.weld_type = weld_type
        self.dim = dim
        self._compiled_expr: Optional[Callable[..., Any]] = None
        if isinstance(expr, str):
            # Compile the string once to avoid repeated parsing.
            try:
                self._compiled_expr = eval(expr, {"__builtins__": {}})
            except Exception:
                # If eval fails, keep the string and let evaluate handle it.
                self._compiled_expr = None

    def _apply_passes(
        self,
        result: Any,
        passes: Iterable[Callable[[Any], Any]],
    ) -> Any:
        """Apply a sequence of transformation passes to the result."""
        for p in passes:
            try:
                result = p(result)
            except Exception as exc:
                raise RuntimeError(
                    f"Pass {p!r} raised an exception: {exc}"
                ) from exc
        return result

    def _apply_experimental_transforms(self, result: Any) -> Any:
        """Apply a dummy experimental transform (reverse string or list)."""
        if isinstance(result, (str, bytes)):
            return result[::-1]
        if isinstance(result, list):
            return list(reversed(result))
        return result

    def evaluate(
        self,
        verbose: bool = True,
        decode: bool = True,
        passes: Optional[Iterable[Callable[[Any], Any]]] = None,
        num_threads: int = 1,
        apply_experimental_transforms: bool = False,
    ) -> Any:
        """
        Evaluate the stored expression and optionally apply transformation passes.

        Parameters
        ----------
        verbose
            If ``True``, print progress information.
        decode
            If ``True`` and the result is ``bytes``, decode it to ``utf-8``.
        passes
            An iterable of callables that take the current result and return a
            transformed result. If ``None``, no passes are applied.
        num_threads
            Number of worker threads to use when applying passes in parallel.
            Only used if ``passes`` is a list with more than one element.
        apply_experimental_transforms
            If ``True``, apply a simple experimental transform after all passes.

        Returns
        -------
        Any
            The final evaluated and transformed result.
        """
        if verbose:
            print(
                f"[LazyOpResult] Starting evaluation of {self.weld_type} (dim={self.dim})")

        # Step 1: Evaluate the expression
        try:
            if self._compiled_expr is not None:
                result = self._compiled_expr
            elif callable(self.expr):
                result = self.expr()
            else:
                # Treat expr as a string expression
                result = eval(self.expr, {"__builtins__": {}})
        except Exception as exc:
            tb = traceback.format_exc()
            raise RuntimeError(
                f"Failed to evaluate expression: {exc}\n{tb}") from exc

        if verbose:
            print(f"[LazyOpResult] Initial result: {result!r}")

        # Step 2: Apply passes
        if passes:
            passes_list = list(passes)
            if verbose:
                print(
                    f"[LazyOpResult] Applying {len(passes_list)} passes with {num_threads} thread(s)")
            if num_threads > 1 and len(passes_list) > 1:
                # Parallel application of passes
                with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                    future_to_pass = {
                        executor.submit(p, result): p for p in passes_list
                    }
                    for future in concurrent.futures.as_completed(future_to_pass):
                        p = future_to_pass[future]
                        try:
                            result = future.result()
                        except Exception as exc:
                            raise RuntimeError(
                                f"Pass {p!r} raised an exception in thread: {exc}"
                            ) from exc
            else:
                # Sequential application
                result = self._apply_passes(result, passes_list)

            if verbose:
                print(f"[LazyOpResult] Result after passes: {result!r}")

        # Step 3: Experimental transforms
        if apply_experimental_transforms:
            if verbose:
                print("[LazyOpResult] Applying experimental transforms")
            result = self._apply_experimental_transforms(result)
            if verbose:
                print(
                    f"[LazyOpResult] Result after experimental transforms: {result!r}")

        # Step 4: Decode if needed
        if decode and isinstance(result, bytes):
            try:
                result = result.decode("utf-8")
                if verbose:
                    print("[LazyOpResult] Decoded bytes to string")
            except Exception as exc:
                raise RuntimeError(f"Failed to decode bytes: {exc}") from exc

        if verbose:
            print("[LazyOpResult] Evaluation complete")

        return result
