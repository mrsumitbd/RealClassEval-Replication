from typing import Optional, List, Dict, Any, Iterable


class ComputeBackendValidatorBase:
    '''REANA workflow compute backend validation base class.'''

    def __init__(self, workflow_steps: Optional[List[Dict]] = None, supported_backends: Optional[List[str]] = []):
        '''Validate compute backends in REANA workflow steps.
        :param workflow_steps: list of dictionaries which represents different steps involved in workflow.
        :param supported_backends: a list of the supported compute backends.
        '''
        # Avoid mutable default pitfalls
        self.workflow_steps: List[Dict[str, Any]] = list(workflow_steps or [])
        self.supported_backends: List[str] = list(supported_backends or [])
        # Normalized set for comparison (case-insensitive)
        self._supported_norm = {self._normalize_backend(
            b) for b in self.supported_backends if isinstance(b, str)}

    def validate(self) -> None:
        '''Validate compute backends in REANA workflow.'''
        if not self.workflow_steps or not self._supported_norm:
            return

        for idx, step in enumerate(self.workflow_steps):
            step_name = self._extract_step_name(step, idx)
            for backend in self._extract_compute_backends(step):
                norm_backend = self._normalize_backend(backend)
                if norm_backend not in self._supported_norm:
                    self.raise_error(backend, step_name)

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        '''Raise validation error.'''
        supported = ", ".join(sorted(self.supported_backends))
        msg = (
            f"Unsupported compute backend '{compute_backend}' in step '{step_name}'. "
            f"Supported backends are: {supported or 'none'}."
        )
        raise ValueError(msg)

    def _extract_step_name(self, step: Dict[str, Any], index: int) -> str:
        return str(step.get("name") or step.get("id") or f"step_{index}")

    def _extract_compute_backends(self, step: Dict[str, Any]) -> List[str]:
        # Possible locations and shapes of compute backend info
        candidates: List[Any] = []

        # Direct key
        if "compute_backend" in step:
            candidates.append(step.get("compute_backend"))

        # Nested common structures
        for key in ("resources", "scheduler", "compute", "hints", "runner"):
            nested = step.get(key)
            if isinstance(nested, dict) and "compute_backend" in nested:
                candidates.append(nested.get("compute_backend"))

        # Flatten and normalize to list of strings
        backends: List[str] = []
        for c in candidates:
            if c is None:
                continue
            if isinstance(c, str):
                if c.strip():
                    backends.append(c.strip())
            elif isinstance(c, (list, tuple, set)):
                for item in c:
                    if isinstance(item, str) and item.strip():
                        backends.append(item.strip())
            elif isinstance(c, dict):
                # Some formats might provide {type: "kubernetes"} or similar
                for k in ("type", "name", "backend"):
                    v = c.get(k)
                    if isinstance(v, str) and v.strip():
                        backends.append(v.strip())
        # Deduplicate while preserving order
        seen = set()
        result: List[str] = []
        for b in backends:
            lb = b.lower()
            if lb not in seen:
                seen.add(lb)
                result.append(b)
        return result

    def _normalize_backend(self, backend: Optional[str]) -> str:
        return (backend or "").strip().lower()
