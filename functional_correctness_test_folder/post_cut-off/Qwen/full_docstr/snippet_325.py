
from pathlib import Path
from typing import Literal, Optional
from types import ModuleType


class YamlAgentDocument:
    # Assuming YamlAgentDocument is a class that holds YAML agent data
    def __init__(self, data: dict):
        self.data = data


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(self, name: str, description: str, file_path: Optional[Path] = None, module: Optional[ModuleType] = None, yaml_document: Optional[YamlAgentDocument] = None) -> None:
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
        else:
            raise ValueError("AgentInfo does not have a file path defined")
