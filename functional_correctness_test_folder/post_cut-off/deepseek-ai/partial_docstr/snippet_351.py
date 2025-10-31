
from pathlib import Path
from types import ModuleType
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .yaml_agent_document import YamlAgentDocument


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(self, name: str, description: str, file_path: Path | None = None, module: 'ModuleType | None' = None, yaml_document: 'YamlAgentDocument | None' = None) -> None:
        self._name = name
        self._description = description
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        if self._module is not None:
            return 'python'
        elif self._yaml_document is not None:
            return 'yaml'
        else:
            raise ValueError(
                "AgentInfo must have either a module or a YAML document.")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self._file_path is not None:
            return str(self._file_path)
        elif self._yaml_document is not None and hasattr(self._yaml_document, 'file_path'):
            return str(self._yaml_document.file_path)
        else:
            raise ValueError("No valid path found for the agent.")
