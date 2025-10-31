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

        # name validation
        if not isinstance(self.name, str):
            errors.append("name must be a string.")
        elif not self.name.strip():
            errors.append("name cannot be empty.")

        # file_path validation
        if not isinstance(self.file_path, str):
            errors.append("file_path must be a string.")
        elif not self.file_path.strip():
            errors.append("file_path cannot be empty.")

        # metadata validation
        if not isinstance(self.metadata, dict):
            errors.append("metadata must be a dict.")

        # content validation
        if not isinstance(self.content, str):
            errors.append("content must be a string.")

        return errors
