
import os
from typing import Any, Dict, List, Optional


class WorkflowDefinition:
    """Simple container for workflow data."""

    def __init__(self, name: str, file_path: str, metadata: Dict[str, Any], content: str):
        """
        Initialize a workflow definition.

        Args:
            name (str): Name of the workflow.
            file_path (str): Path to the workflow file.
            metadata (dict): Metadata from the frontmatter.
            content (str): Content of the workflow file.
        """
        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self) -> List[str]:
        """
        Basic validation of required fields.

        Returns:
            list: List of validation errors.
        """
        errors: List[str] = []

        # Validate name
        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("Workflow 'name' must be a non-empty string.")

        # Validate file_path
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append("Workflow 'file_path' must be a non-empty string.")
        else:
            # Optional: check that the path is a file (if desired)
            if not os.path.isfile(self.file_path):
                errors.append(
                    f"Workflow file '{self.file_path}' does not exist or is not a file.")

        # Validate metadata
        if not isinstance(self.metadata, dict):
            errors.append("Workflow 'metadata' must be a dictionary.")
        else:
            # Common required keys in metadata
            required_meta_keys = ["description", "author", "steps"]
            for key in required_meta_keys:
                if key not in self.metadata:
                    errors.append(f"Metadata missing required key: '{key}'.")

            # Validate steps
            steps = self.metadata.get("steps")
            if steps is not None:
                if not isinstance(steps, list):
                    errors.append("Metadata 'steps' must be a list.")
                else:
                    for idx, step in enumerate(steps):
                        if not isinstance(step, dict):
                            errors.append(
                                f"Step {idx} in 'steps' must be a dictionary.")
                            continue
                        if "name" not in step:
                            errors.append(
                                f"Step {idx} missing required 'name' field.")
                        if "type" not in step:
                            errors.append(
                                f"Step {idx} missing required 'type' field.")

        # Validate content
        if not isinstance(self.content, str) or not self.content.strip():
            errors.append("Workflow 'content' must be a non-empty string.")

        return errors
