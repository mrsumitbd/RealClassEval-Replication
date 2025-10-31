
import os


class WorkflowDefinition:
    def __init__(self, name, file_path, metadata, content):
        self.name = name
        self.file_path = file_path
        self.metadata = metadata
        self.content = content

    def validate(self):
        errors = []

        # Validate name
        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("Name must be a non-empty string.")

        # Validate file_path
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append("File path must be a non-empty string.")
        elif not os.path.isfile(self.file_path):
            errors.append(f"File '{self.file_path}' does not exist.")

        # Validate metadata
        if not isinstance(self.metadata, dict):
            errors.append("Metadata must be a dictionary.")
        else:
            # Example: metadata must contain a 'version' key
            if 'version' not in self.metadata:
                errors.append("Metadata must contain a 'version' key.")

        # Validate content
        if not isinstance(self.content, str) or not self.content.strip():
            errors.append("Content must be a non-empty string.")

        if errors:
            raise ValueError("Validation failed: " + "; ".join(errors))

        return True
