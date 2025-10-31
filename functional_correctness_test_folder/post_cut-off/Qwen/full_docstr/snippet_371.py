
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
        if not isinstance(self.name, str) or not self.name:
            errors.append("Name must be a non-empty string.")
        if not isinstance(self.file_path, str) or not self.file_path:
            errors.append("File path must be a non-empty string.")
        if not isinstance(self.metadata, dict):
            errors.append("Metadata must be a dictionary.")
        if not isinstance(self.content, str):
            errors.append("Content must be a string.")
        return errors
