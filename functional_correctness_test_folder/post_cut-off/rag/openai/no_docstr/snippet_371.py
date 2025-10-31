
import os
from typing import List, Dict, Any


class WorkflowDefinition:
    '''Simple container for workflow data.'''

    def __init__(self, name: str, file_path: str, metadata: Dict[str, Any], content: str):
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

    def validate(self) -> List[str]:
        '''Basic validation of required fields.
        Returns:
            list: List of validation errors.
        '''
        errors: List[str] = []

        # Validate name
        if not isinstance(self.name, str) or not self.name.strip():
            errors.append('Workflow name must be a non-empty string.')

        # Validate file_path
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append('File path must be a non-empty string.')
        elif not os.path.isfile(self.file_path):
            errors.append(
                f'File path does not exist or is not a file: {self.file_path}')

        # Validate metadata
        if not isinstance(self.metadata, dict):
            errors.append('Metadata must be a dictionary.')
        else:
            # Optional: ensure metadata contains a 'steps' key that is a list
            if 'steps' not in self.metadata:
                errors.append('Metadata missing required key: "steps".')
            elif not isinstance(self.metadata['steps'], list):
                errors.append('Metadata "steps" must be a list.')

        # Validate content
        if not isinstance(self.content, str):
            errors.append('Content must be a string.')

        return errors
