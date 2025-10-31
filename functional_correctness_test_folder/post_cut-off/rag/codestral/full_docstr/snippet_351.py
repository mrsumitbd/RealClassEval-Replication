
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional, Union


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(self, name: str, description: str, file_path: Optional[Union[Path, str]] = None, module: Optional[ModuleType] = None, yaml_document: Optional['YamlAgentDocument'] = None) -> None:
        '''Initialize agent info.
        Args:
            name: Agent name
            description: Agent description
            file_path: Path to agent file/directory
            module: Python module (for Python agents)
            yaml_document: YAML agent document (for YAML agents)
        '''
        self.name = name
        self.description = description
        self.file_path = Path(file_path) if file_path else None
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
            raise ValueError('Agent kind could not be determined')

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)
        else:
            raise ValueError('Agent path is not set')
