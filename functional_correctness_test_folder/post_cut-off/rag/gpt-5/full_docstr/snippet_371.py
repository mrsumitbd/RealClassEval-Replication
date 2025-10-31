from copy import deepcopy


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
        self.metadata = deepcopy(metadata) if isinstance(
            metadata, dict) else metadata
        self.content = content

    def validate(self):
        '''Basic validation of required fields.
        Returns:
            list: List of validation errors.
        '''
        errors = []

        if not isinstance(self.name, str) or not self.name.strip():
            errors.append("Field 'name' must be a non-empty string.")

        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append("Field 'file_path' must be a non-empty string.")

        if not isinstance(self.metadata, dict):
            errors.append("Field 'metadata' must be a dict.")
        else:
            # Optional type checks for common metadata fields if present
            meta = self.metadata
            if 'id' in meta and not isinstance(meta['id'], str):
                errors.append("Metadata field 'id' must be a string.")
            if 'version' in meta and not isinstance(meta['version'], (str, int, float)):
                errors.append(
                    "Metadata field 'version' must be a string or number.")
            if 'tags' in meta:
                tags = meta['tags']
                if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
                    errors.append(
                        "Metadata field 'tags' must be a list of strings.")
            if 'steps' in meta and not isinstance(meta['steps'], list):
                errors.append("Metadata field 'steps' must be a list.")

        if not isinstance(self.content, str) or not self.content.strip():
            errors.append("Field 'content' must be a non-empty string.")

        return errors
