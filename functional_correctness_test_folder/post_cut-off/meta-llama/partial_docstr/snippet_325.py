
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional


class YamlAgentDocument:
    # Assuming YamlAgentDocument is defined elsewhere
    pass


class AgentInfo:

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

        if (self.module is not None and self.yaml_document is not None) or (self.module is None and self.yaml_document is None):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided")

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        if self.module is not None:
            return 'python'
        else:
            return 'yaml'

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.kind == 'python':
            if self.module is None:
                raise ValueError("Module is not defined")
            return self.module.__file__ if self.module.__file__ is not None else ''
        else:
            if self.file_path is None:
                raise ValueError("File path is not defined")
            return str(self.file_path)
