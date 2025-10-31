
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
        self.file_path = file_path
        self.module = module
        self.yaml_document = yaml_document

        # Validation: exactly one of module or yaml_document must be provided
        if (module is None) == (yaml_document is None):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided"
            )

    @property
    def kind(self) -> Literal["python", "yaml"]:
        '''Get the definition type of the agent.'''
        return "python" if self.module is not None else "yaml"

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)
        if self.module is not None:
            return getattr(self.module, "__file__", "")
        if self.yaml_document is not None:
            # Prefer a 'path' attribute, fall back to 'file_path'
            return getattr(self.yaml_document, "path", getattr(self.yaml_document, "file_path", ""))
        return ""
