
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
            errors.append("Workflow 'name' must be a non-empty string.")

        # Validate file_path
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append("Workflow 'file_path' must be a non-empty string.")

        # Validate metadata
        if not isinstance(self.metadata, dict):
            errors.append("Workflow 'metadata' must be a dictionary.")
        else:
            # Basic required keys in metadata
            if 'steps' not in self.metadata:
                errors.append("Metadata must contain a 'steps' key.")
            else:
                steps = self.metadata['steps']
                if not isinstance(steps, list):
                    errors.append("'steps' in metadata must be a list.")
                else:
                    for idx, step in enumerate(steps):
                        if not isinstance(step, dict):
                            errors.append(f"Step {idx} must be a dictionary.")
                            continue
                        if 'name' not in step:
                            errors.append(
                                f"Step {idx} missing required 'name' field.")
                        if 'type' not in step:
                            errors.append(
                                f"Step {idx} missing required 'type' field.")

        # Validate content
        if not isinstance(self.content, str) or not self.content.strip():
            errors.append("Workflow 'content' must be a non-empty string.")

        return errors
