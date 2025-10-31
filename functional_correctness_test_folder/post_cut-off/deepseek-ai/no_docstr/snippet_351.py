
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .yaml_agent_document import YamlAgentDocument


class AgentInfo:

    def __init__(self, name: str, description: str, file_path: Optional[Path] = None, module: Optional[ModuleType] = None, yaml_document: Optional['YamlAgentDocument'] = None) -> None:
        self._name = name
        self._description = description
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document

    @property
    def kind(self) -> Literal['python', 'yaml']:
        if self._module is not None:
            return 'python'
        else:
            return 'yaml'

    @property
    def path(self) -> str:
        if self._file_path is not None:
            return str(self._file_path)
        elif self._yaml_document is not None and hasattr(self._yaml_document, 'file_path'):
            return str(self._yaml_document.file_path)
        else:
            raise ValueError("No path available for the agent")
