from typing import Dict, List, Optional
from reana_commons.errors import REANAValidationError

class ComputeBackendValidatorBase:
    """REANA workflow compute backend validation base class."""

    def __init__(self, workflow_steps: Optional[List[Dict]]=None, supported_backends: Optional[List[str]]=[]):
        """Validate compute backends in REANA workflow steps.

        :param workflow_steps: list of dictionaries which represents different steps involved in workflow.
        :param supported_backends: a list of the supported compute backends.
        """
        self.workflow_steps = workflow_steps
        self.supported_backends = supported_backends

    def validate(self) -> None:
        """Validate compute backends in REANA workflow."""
        raise NotImplementedError

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        """Raise validation error."""
        raise REANAValidationError(f'''Compute backend "{compute_backend}" found in step "{step_name}" is not supported. List of supported compute backends: "{', '.join(self.supported_backends)}"''')