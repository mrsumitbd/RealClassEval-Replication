
from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional

# Forward declaration for type checking
try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from yaml_agent_document import YamlAgentDocument  # noqa: F401
except Exception:
    YamlAgentDocument = None  # type: ignore


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Optional[Path] = None,
        module: Optional[ModuleType] = None,
        yaml_document: Optional["YamlAgentDocument"] = None,
    ) -> None:
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
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document

    @property
    def kind(self) -> Literal["python", "yaml"]:
        '''Get the definition type of the agent.'''
        if self._module is not None:
            return "python"
        if self._yaml_document is not None:
            return "yaml"
        raise ValueError(
            "AgentInfo must have either a module or a yaml_document")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self._file_path is not None:
            return str(self._file_path)
        if self._module is not None:
            return getattr(self._module, "__file__", "")
        if self._yaml_document is not None:
            # Assume YamlAgentDocument exposes a `path` attribute
            return getattr(self._yaml_document, "path", "")
        return ""
