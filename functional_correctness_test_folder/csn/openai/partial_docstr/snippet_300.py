
from typing import List, Dict, Optional


class ComputeBackendValidatorBase:
    """
    Validate compute backends in REANA workflow steps.

    Parameters
    ----------
    workflow_steps : Optional[List[Dict]]
        List of dictionaries representing the steps in a REANA workflow.
    supported_backends : Optional[List[str]]
        List of supported compute backends. Defaults to an empty list.
    """

    def __init__(
        self,
        workflow_steps: Optional[List[Dict]] = None,
        supported_backends: Optional[List[str]] = None,
    ):
        self.workflow_steps = workflow_steps or []
        self.supported_backends = supported_backends or []

    def validate(self) -> None:
        """
        Validate that each workflow step uses a supported compute backend.
        Raises a ValueError if an unsupported backend is found.
        """
        for step in self.workflow_steps:
            step_name = step.get("name", "<unknown>")
            compute_backend = step.get("compute_backend")

            # Skip validation if no backend is specified
            if compute_backend is None:
                continue

            if compute_backend not in self.supported_backends:
                self.raise_error(compute_backend, step_name)

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        """
        Raise a ValueError indicating that the compute backend is unsupported.

        Parameters
        ----------
        compute_backend : str
            The unsupported compute backend.
        step_name : str
            The name of the workflow step that uses the unsupported backend.
        """
        msg = (
            f"Unsupported compute backend '{compute_backend}' "
            f"used in step '{step_name}'. "
            f"Supported backends are: {', '.join(self.supported_backends) or 'none'}."
        )
        raise ValueError(msg)
