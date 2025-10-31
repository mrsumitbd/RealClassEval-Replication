
class ComputeBackendValidatorBase:
    '''REANA workflow compute backend validation base class.'''

    def __init__(self, workflow_steps: Optional[List[Dict]] = None, supported_backends: Optional[List[str]] = []):
        '''Validate compute backends in REANA workflow steps.
        :param workflow_steps: list of dictionaries which represents different steps involved in workflow.
        :param supported_backends: a list of the supported compute backends.
        '''
        self.workflow_steps = workflow_steps or []
        self.supported_backends = supported_backends or []

    def validate(self) -> None:
        '''Validate compute backends in REANA workflow.'''
        for step in self.workflow_steps:
            if 'backend' in step:
                compute_backend = step['backend']
                if compute_backend not in self.supported_backends:
                    self.raise_error(
                        compute_backend, step.get('name', 'unknown'))

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        '''Raise validation error.'''
        raise ValueError(
            f"Unsupported compute backend '{compute_backend}' in step '{step_name}'")
