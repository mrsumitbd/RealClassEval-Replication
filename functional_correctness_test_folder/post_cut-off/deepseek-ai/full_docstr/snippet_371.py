
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
        if not self.name:
            errors.append("Name is required.")
        if not self.file_path:
            errors.append("File path is required.")
        if not isinstance(self.metadata, dict):
            errors.append("Metadata must be a dictionary.")
        if not self.content:
            errors.append("Content is required.")
        return errors
