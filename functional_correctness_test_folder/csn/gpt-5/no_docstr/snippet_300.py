from typing import List, Dict, Optional


class ComputeBackendValidatorBase:
    def __init__(self, workflow_steps: Optional[List[Dict]] = None, supported_backends: Optional[List[str]] = []):
        self.workflow_steps: List[Dict] = list(
            workflow_steps) if workflow_steps is not None else []
        self.supported_backends: List[str] = list(
            supported_backends) if supported_backends is not None else []

    def validate(self) -> None:
        if not self.workflow_steps:
            return
        for idx, step in enumerate(self.workflow_steps):
            if not isinstance(step, dict):
                raise TypeError(
                    f"Workflow step at index {idx} must be a dict, got {type(step).__name__}")
            step_name = str(step.get("name", f"step_{idx}"))
            compute_backend = step.get("compute_backend")
            if compute_backend is None:
                self.raise_error("<missing>", step_name)
            if self.supported_backends and compute_backend not in self.supported_backends:
                self.raise_error(str(compute_backend), step_name)

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        supported = ", ".join(
            self.supported_backends) if self.supported_backends else "none"
        raise ValueError(
            f"Unsupported compute backend '{compute_backend}' for step '{step_name}'. "
            f"Supported backends: {supported}."
        )
