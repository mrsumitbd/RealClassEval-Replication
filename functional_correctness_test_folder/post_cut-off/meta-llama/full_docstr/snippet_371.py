
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
        validation_errors = []
        required_fields = ['name', 'description']

        if not self.name:
            validation_errors.append('Name is required')

        for field in required_fields:
            if field not in self.metadata or not self.metadata[field]:
                validation_errors.append(
                    f'{field.capitalize()} is required in metadata')

        return validation_errors
