
from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional

# Forward declaration for type checking
try:
    from .yaml_agent_document import YamlAgentDocument  # type: ignore
except Exception:
    YamlAgentDocument = None  # pragma: no cover


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

        # Basic validation: exactly one of module or yaml_document must be provided
        if (module is None) == (yaml_document is None):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided."
            )

    @property
    def kind(self) -> Literal["python", "yaml"]:
        '''Get the definition type of the agent.'''
        if self.module is not None:
            return "python"
        if self.yaml_document is not None:
            return "yaml"
        raise ValueError("Agent kind cannot be determined.")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)
        if self.module is not None:
            return getattr(self.module, "__file__", "")
        if self.yaml_document is not None:
            # Assume yaml_document has a 'path' attribute if available
            return getattr(self.yaml_document, "path", "")
        return ""
