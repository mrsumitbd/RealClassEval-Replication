from __future__ import annotations

from pathlib import Path
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Any


class AgentInfo:
    """Agent information container supporting both Python and YAML agents."""

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Path | None = None,
        module: "ModuleType | None" = None,
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
        if (module is None) == (yaml_document is None):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided.")

        self.name = name
        self.description = description
        self.module = module
        self.yaml_document = yaml_document

        resolved_path = file_path

        if resolved_path is None and module is not None:
            # Try to resolve path from Python module/package
            path_str = getattr(module, "__file__", None)
            if not path_str:
                mod_path = getattr(module, "__path__", None)  # packages
                if mod_path:
                    try:
                        path_str = list(mod_path)[0]  # type: ignore[index]
                    except Exception:
                        path_str = None
            if path_str:
                resolved_path = Path(path_str)

        if resolved_path is None and yaml_document is not None:
            # Try common attribute names that may hold the source path
            for attr in ("path", "file_path", "source_path", "uri", "source"):
                if hasattr(yaml_document, attr):
                    val = getattr(yaml_document, attr)
                    if isinstance(val, Path):
                        resolved_path = val
                        break
                    if isinstance(val, str) and val:
                        resolved_path = Path(val)
                        break

        self.file_path = resolved_path

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Get the definition type of the agent."""
        return "python" if self.module is not None else "yaml"

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        return str(self.file_path) if self.file_path is not None else ""
