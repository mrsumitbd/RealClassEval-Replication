from typing import Optional, List, Dict


class ComputeBackendValidatorBase:

    def __init__(self, workflow_steps: Optional[List[Dict]] = None, supported_backends: Optional[List[str]] = None):
        '''Validate compute backends in REANA workflow steps.
        :param workflow_steps: list of dictionaries which represents different steps involved in workflow.
        :param supported_backends: a list of the supported compute backends.
        '''
        self.workflow_steps: List[Dict] = workflow_steps or []
        self.supported_backends: List[str] = supported_backends or []

    def validate(self) -> None:
        for step in self.workflow_steps:
            compute_backend = step.get("compute_backend")
            if not compute_backend:
                continue
            if self.supported_backends and compute_backend not in self.supported_backends:
                step_name = step.get("name", "<unknown>")
                self.raise_error(compute_backend, step_name)

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        supported = ", ".join(
            self.supported_backends) if self.supported_backends else "none"
        raise ValueError(
            f"Unsupported compute backend '{compute_backend}' in step '{step_name}'. "
            f"Supported backends: {supported}."
        )
