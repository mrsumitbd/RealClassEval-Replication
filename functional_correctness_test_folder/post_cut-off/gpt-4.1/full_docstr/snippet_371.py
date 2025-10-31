
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
            errors.append("Workflow name is required and must be a string.")
        if not self.file_path or not isinstance(self.file_path, str):
            errors.append(
                "Workflow file_path is required and must be a string.")
        if not isinstance(self.metadata, dict):
            errors.append("Workflow metadata must be a dictionary.")
        if not self.content or not isinstance(self.content, str):
            errors.append("Workflow content is required and must be a string.")
        return errors
