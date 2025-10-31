from typing import Any, Dict, List
from copy import deepcopy


class WorkflowDefinition:
    '''Simple container for workflow data.'''

    __slots__ = ['name', 'file_path', 'metadata', 'content']

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
        self.metadata = deepcopy(metadata) if isinstance(
            metadata, dict) else metadata
        self.content = content

    def validate(self) -> List[str]:
        '''Basic validation of required fields.
        Returns:
            list: List of validation errors.
        '''
        errors: List[str] = []

        if not isinstance(self.name, str) or not self.name.strip():
            errors.append('name is required and must be a non-empty string.')
        if not isinstance(self.file_path, str) or not self.file_path.strip():
            errors.append(
                'file_path is required and must be a non-empty string.')
        if not isinstance(self.metadata, dict):
            errors.append('metadata must be a dictionary.')
        if not isinstance(self.content, str) or not self.content.strip():
            errors.append(
                'content is required and must be a non-empty string.')

        return errors
