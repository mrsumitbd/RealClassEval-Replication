
from typing import Optional, List, Dict


class ComputeBackendValidatorBase:
    '''REANA workflow compute backend validation base class.'''

    def __init__(self, workflow_steps: Optional[List[Dict]] = None,
                 supported_backends: Optional[List[str]] = None):
        '''Validate compute backends in REANA workflow steps.
        :param workflow_steps: list of dictionaries which represents different steps involved in workflow.
        :param supported_backends: a list of the supported compute backends.
        '''
        self.workflow_steps = workflow_steps or []
        self.supported_backends = supported_backends or []

    def validate(self) -> None:
        '''Validate compute backends in REANA workflow.'''
        for step in self.workflow_steps:
            # Determine step name
            step_name = step.get('name') or step.get(
                'step_name') or '<unknown>'
            # Get compute backend
            compute_backend = step.get('compute_backend')
            if compute_backend is None:
                # If no backend specified, skip or treat as error?
                # Here we skip validation for missing backend.
                continue
            if compute_backend not in self.supported_backends:
                self.raise_error(compute_backend, step_name)

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        '''Raise validation error.'''
        supported = ', '.join(self.supported_backends) or 'none'
        raise ValueError(
            f"Unsupported compute backend '{compute_backend}' in step '{step_name}'. "
            f"Supported backends: {supported}."
        )
