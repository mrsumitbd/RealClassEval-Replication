from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal


class AgentInfo:
    """Agent information container supporting both Python and YAML agents."""

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Path | None = None,
        module: ModuleType | None = None,
        yaml_document: "YamlAgentDocument | None" = None,
    ) -> None:
        """Initialize agent info.
        Args:
            name: Agent name
            description: Agent description
            file_path: Path to agent file/directory
            module: Python module (for Python agents)
            yaml_document: YAML agent document (for YAML agents)
        """
        if module is not None and yaml_document is not None:
            raise ValueError(
                "Provide either 'module' for Python agents or 'yaml_document' for YAML agents, not both.")
        self.name = name
        self.description = description
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Get the definition type of the agent."""
        if self._module is not None:
            return "python"
        if self._yaml_document is not None:
            return "yaml"
        if self._file_path is not None:
            suffix = self._file_path.suffix.lower()
            return "yaml" if suffix in (".yaml", ".yml") else "python"
        raise ValueError(
            "Cannot determine agent kind: no module, yaml_document, or file_path provided.")

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self._file_path is not None:
            return str(self._file_path)

        if self._module is not None:
            module_file = getattr(self._module, "__file__", None)
            if module_file:
                return str(module_file)

        if self._yaml_document is not None:
            for attr in ("path", "file_path", "file", "uri"):
                val = getattr(self._yaml_document, attr, None)
                if val:
                    return str(val)

        raise ValueError("Cannot determine agent path.")
