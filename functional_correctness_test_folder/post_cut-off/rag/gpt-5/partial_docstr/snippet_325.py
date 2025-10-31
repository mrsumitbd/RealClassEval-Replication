from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional
from types import ModuleType


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
        if (module is None) == (yaml_document is None):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided.")

        self.name = name
        self.description = description
        self.module = module
        self.yaml_document = yaml_document

        derived_path: Optional[Path] = None
        if file_path is not None:
            derived_path = file_path
        elif module is not None:
            mod_file = getattr(module, "__file__", None)
            if mod_file:
                derived_path = Path(mod_file)
            else:
                spec = getattr(module, "__spec__", None)
                origin = getattr(
                    spec, "origin", None) if spec is not None else None
                if origin:
                    derived_path = Path(origin)
        elif yaml_document is not None:
            # Try common attributes for path-like references on YAML doc.
            for attr in ("path", "file_path", "source_path", "source", "uri"):
                val = getattr(yaml_document, attr, None)
                if val:
                    if isinstance(val, Path):
                        derived_path = val
                    else:
                        try:
                            derived_path = Path(str(val))
                        except Exception:
                            pass
                    if derived_path:
                        break

        self.file_path = derived_path

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Get the definition type of the agent."""
        return "python" if self.module is not None else "yaml"

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self.file_path is not None:
            return str(self.file_path)
        if self.module is not None:
            # Fallbacks if file path couldn't be derived earlier.
            mod_file = getattr(self.module, "__file__", None)
            if mod_file:
                return str(mod_file)
            spec = getattr(self.module, "__spec__", None)
            origin = getattr(
                spec, "origin", None) if spec is not None else None
            if origin:
                return str(origin)
        # Last resort: empty string when no path can be determined.
        return ""
