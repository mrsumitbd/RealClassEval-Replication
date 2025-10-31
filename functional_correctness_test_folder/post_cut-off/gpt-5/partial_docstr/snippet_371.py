class WorkflowDefinition:

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
        self.metadata = dict(metadata) if isinstance(
            metadata, dict) else metadata
        self.content = content

    def validate(self):
        '''Basic validation of required fields.
        Returns:
            list: List of validation errors.
        '''
        errors = []

        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("Invalid 'name': must be a non-empty string.")

        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append("Invalid 'file_path': must be a non-empty string.")

        if self.metadata is None:
            errors.append("Invalid 'metadata': must be a dict, got None.")
        elif not isinstance(self.metadata, dict):
            errors.append(
                f"Invalid 'metadata': must be a dict, got {type(self.metadata).__name__}.")

        if not isinstance(self.content, str):
            errors.append(
                f"Invalid 'content': must be a string, got {type(self.content).__name__}.")
        elif self.content == "":
            errors.append("Invalid 'content': must not be empty.")

        return errors
