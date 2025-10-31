
from typing import List, Dict, Optional


class ComputeBackendValidatorBase:
    '''REANA workflow compute backend validation base class.'''

    def __init__(self, workflow_steps: Optional[List[Dict]] = None, supported_backends: Optional[List[str]] = None):
        '''Validate compute backends in REANA workflow steps.
        :param workflow_steps: list of dictionaries which represents different steps involved in workflow.
        :param supported_backends: a list of the supported compute backends.
        '''
        self.workflow_steps = workflow_steps if workflow_steps is not None else []
        self.supported_backends = supported_backends if supported_backends is not None else []

    def validate(self) -> None:
        '''Validate compute backends in REANA workflow.'''
        for step in self.workflow_steps:
            compute_backend = step.get('compute_backend')
            if compute_backend and compute_backend not in self.supported_backends:
                self.raise_error(compute_backend, step.get(
                    'name', 'unnamed_step'))

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        '''Raise validation error.'''
        raise ValueError(
            f"Compute backend '{compute_backend}' in step '{step_name}' is not supported. "
            f"Supported backends are: {', '.join(self.supported_backends)}"
        )
