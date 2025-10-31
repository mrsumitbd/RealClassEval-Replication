
from typing import Optional, List, Dict


class ComputeBackendValidatorBase:

    def __init__(self, workflow_steps: Optional[List[Dict]] = None, supported_backends: Optional[List[str]] = []):
        self.workflow_steps = workflow_steps if workflow_steps is not None else []
        self.supported_backends = supported_backends if supported_backends is not None else []

    def validate(self) -> None:
        for step in self.workflow_steps:
            compute_backend = step.get('compute_backend')
            step_name = step.get('name')
            if compute_backend not in self.supported_backends:
                self.raise_error(compute_backend, step_name)

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        raise ValueError(
            f"Unsupported compute backend '{compute_backend}' for step '{step_name}'. Supported backends are: {', '.join(self.supported_backends)}")
