
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional


class YamlAgentDocument:
    # Assuming YamlAgentDocument is a class that holds YAML agent data
    def __init__(self, data: dict):
        self.data = data


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(self, name: str, description: str, file_path: Optional[Path] = None, module: Optional[ModuleType] = None, yaml_document: Optional[YamlAgentDocument] = None) -> None:
        self.name = name
        self.description = description
        self.file_path = file_path
        self.module = module
        self.yaml_document = yaml_document

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        if self.module is not None:
            return 'python'
        elif self.yaml_document is not None:
            return 'yaml'
        else:
            raise ValueError(
                "AgentInfo must be initialized with either a module or a yaml_document")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)
        elif self.yaml_document is not None:
            # Assuming yaml_document has a path attribute or similar
            return self.yaml_document.data.get('path', 'No path specified')
        else:
            return 'No path available'
