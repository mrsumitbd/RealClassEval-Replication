
import os


class WorkflowDefinition:
    '''Simple container for workflow data.'''

    def __init__(self, name, file_path, metadata, content):
        '''Initialize a workflow definition.
        Args:
            name (str): Name of the workflow.
            file_path (str): Path to the workflow file.
            metadata (dict): Metadata from the frontmatter.
            content (str): Content of the workflow file.
        '''
        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self):
        '''Basic validation of required fields.
        Returns:
            list: List of validation errors.
        '''
        errors = []

        # Validate name
        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("Workflow name must be a non-empty string.")

        # Validate file_path
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append("File path must be a non-empty string.")
        elif not os.path.isfile(self.file_path):
            errors.append(
                f"File path does not exist or is not a file: {self.file_path}")

        # Validate metadata
        if not isinstance(self.metadata, dict):
            errors.append("Metadata must be a dictionary.")
        else:
            # Optional: ensure required metadata keys exist
            required_meta_keys = ["author", "version"]
            missing_keys = [
                k for k in required_meta_keys if k not in self.metadata]
            if missing_keys:
                errors.append(
                    f"Metadata missing required keys: {', '.join(missing_keys)}")

        # Validate content
        if not isinstance(self.content, str) or not self.content.strip():
            errors.append("Content must be a non-empty string.")

        return errors
