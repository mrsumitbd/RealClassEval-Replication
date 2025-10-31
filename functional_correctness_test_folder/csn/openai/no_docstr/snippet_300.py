
from typing import Optional, List, Dict


class ComputeBackendValidatorBase:
    """
    Base class for validating compute backends used in workflow steps.
    """

    def __init__(
        self,
        workflow_steps: Optional[List[Dict]] = None,
        supported_backends: Optional[List[str]] = None,
    ):
        """
        Parameters
        ----------
        workflow_steps : Optional[List[Dict]]
            A list of dictionaries, each representing a workflow step.
            Each step dictionary is expected to contain at least the keys
            'name' (or 'step_name') and 'compute_backend'.
        supported_backends : Optional[List[str]]
            A list of compute backend names that are considered valid.
        """
        self.workflow_steps: List[Dict] = workflow_steps or []
        self.supported_backends: List[str] = supported_backends or []

    def validate(self) -> None:
        """
        Validate that every workflow step uses a supported compute backend.
        Raises a ValueError if an unsupported backend is found.
        """
        for step in self.workflow_steps:
            # Determine step name
            step_name = step.get("name") or step.get(
                "step_name") or "<unknown>"
            # Determine compute backend
            compute_backend = step.get(
                "compute_backend") or step.get("backend")
            if compute_backend is None:
                # If no backend specified, skip or treat as error?
                # Here we treat missing backend as an error.
                self.raise_error("<missing>", step_name)
                continue

            if compute_backend not in self.supported_backends:
                self.raise_error(compute_backend, step_name)

    def raise_error(self, compute_backend: str, step_name: str) -> None:
        """
        Raise a ValueError indicating that the given compute backend is not supported
        for the specified step.

        Parameters
        ----------
        compute_backend : str
            The compute backend that was found in the step.
        step_name : str
            The name of the step where the unsupported backend was found.
        """
        supported = ", ".join(self.supported_backends) or "none"
        message = (
            f"Unsupported compute backend '{compute_backend}' for step '{step_name}'. "
            f"Supported backends: {supported}."
        )
        raise ValueError(message)
