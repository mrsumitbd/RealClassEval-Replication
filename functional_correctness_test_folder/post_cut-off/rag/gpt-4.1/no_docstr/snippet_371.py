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
        if not self.name or not isinstance(self.name, str):
            errors.append("Missing or invalid 'name'.")
        if not self.file_path or not isinstance(self.file_path, str):
            errors.append("Missing or invalid 'file_path'.")
        if not isinstance(self.metadata, dict):
            errors.append("Missing or invalid 'metadata'.")
        if not self.content or not isinstance(self.content, str):
            errors.append("Missing or invalid 'content'.")
        return errors
