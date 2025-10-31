
from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any, Literal, Optional


class AgentInfo:
    def __init__(
        self,
        name: str,
        description: str,
        file_path: Optional[Path] = None,
        module: Optional[ModuleType] = None,
        yaml_document: Optional[Any] = None,
    ) -> None:
        """
        Initialize agent info.

        Args:
            name: Agent name
            description: Agent description
            file_path: Path to agent file/directory
            module: Python module (for Python agents)
            yaml_document: YAML agent document (for YAML agents)
        """
        self.name = name
        self.description = description
        self.file_path = file_path
        self.module = module
        self.yaml_document = yaml_document

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Get the definition type of the agent."""
        if self.module is not None:
            return "python"
        if self.yaml_document is not None:
            return "yaml"
        raise ValueError(
            "AgentInfo must have either a module or a yaml_document")

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self.file_path is not None:
            return str(self.file_path)
        if self.module is not None:
            # module.__file__ may be None for built‑in modules
            return getattr(self.module, "__file__", "")
        if self.yaml_document is not None:
            # Assume yaml_document has a `path` attribute
            return getattr(self.yaml_document, "path", "")
        return ""
