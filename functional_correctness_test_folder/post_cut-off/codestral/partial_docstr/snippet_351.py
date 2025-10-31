
from pathlib import Path
from types import ModuleType
from typing import Literal, Union


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(self, name: str, description: str, file_path: Union[Path, None] = None, module: Union[ModuleType, None] = None, yaml_document: Union['YamlAgentDocument', None] = None) -> None:
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
            raise ValueError("Agent kind could not be determined.")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)
        else:
            raise ValueError("Agent path could not be determined.")
