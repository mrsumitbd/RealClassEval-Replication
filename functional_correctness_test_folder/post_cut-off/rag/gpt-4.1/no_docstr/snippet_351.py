from pathlib import Path
from types import ModuleType
from typing import Literal


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Path | None = None,
        module: 'ModuleType | None' = None,
        yaml_document: 'YamlAgentDocument | None' = None
    ) -> None:
        '''
        Initialize agent info.
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
                "AgentInfo must have either a module or a yaml_document.")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)
        elif self.module is not None and hasattr(self.module, '__file__') and self.module.__file__:
            return str(self.module.__file__)
        elif self.yaml_document is not None and hasattr(self.yaml_document, 'file_path'):
            return str(self.yaml_document.file_path)
        else:
            return ""
