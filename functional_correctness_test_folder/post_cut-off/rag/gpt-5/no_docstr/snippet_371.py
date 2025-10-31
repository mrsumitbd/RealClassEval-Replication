class WorkflowDefinition:
    """Simple container for workflow data."""

    def __init__(self, name, file_path, metadata, content):
        """Initialize a workflow definition.
        Args:
            name (str): Name of the workflow.
            file_path (str): Path to the workflow file.
            metadata (dict): Metadata from the frontmatter.
            content (str): Content of the workflow file.
        """
        self.name = name.strip() if isinstance(name, str) else name
        self.file_path = file_path.strip() if isinstance(file_path, str) else file_path
        self.metadata = dict(metadata) if isinstance(
            metadata, dict) else metadata
        self.content = content if isinstance(content, str) else content

    def validate(self):
        """Basic validation of required fields.
        Returns:
            list: List of validation errors.
        """
        errors = []
        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("name must be a non-empty string.")
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append("file_path must be a non-empty string.")
        if not isinstance(self.metadata, dict):
            errors.append("metadata must be a dict.")
        if not isinstance(self.content, str):
            errors.append("content must be a string.")
        elif not self.content.strip():
            errors.append("content cannot be empty.")

        if isinstance(self.metadata, dict):
            meta_name = self.metadata.get("name")
            if isinstance(meta_name, str) and meta_name.strip() and self.name and meta_name.strip() != self.name:
                errors.append(
                    "metadata.name does not match the workflow name.")

        return errors
