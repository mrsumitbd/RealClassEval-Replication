from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional, Any


class AgentInfo:
    """Agent information container supporting both Python and YAML agents."""

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Path | None = None,
        module: ModuleType | None = None,
        yaml_document: Any | None = None,
    ) -> None:
        """Initialize agent info.
        Args:
            name: Agent name
            description: Agent description
            file_path: Path to agent file/directory
            module: Python module (for Python agents)
            yaml_document: YAML agent document (for YAML agents)
        """
        if (module is None and yaml_document is None) or (module is not None and yaml_document is not None):
            raise ValueError(
                "Provide either 'module' or 'yaml_document', but not both.")

        self.name: str = name
        self.description: str = description
        self._file_path: Optional[Path] = file_path
        self.module: Optional[ModuleType] = module
        self.yaml_document: Any | None = yaml_document

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Get the definition type of the agent."""
        if self.module is not None:
            return "python"
        if self.yaml_document is not None:
            return "yaml"
        raise ValueError(
            "Agent kind is undefined: neither module nor yaml_document is set.")

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self._file_path is not None:
            return str(self._file_path)

        if self.kind == "python":
            mod = self.module  # type: ignore[truthy-bool]
            if mod is not None:
                mod_file = getattr(mod, "__file__", None)
                if mod_file:
                    return str(Path(mod_file))
                spec = getattr(mod, "__spec__", None)
                if spec is not None:
                    origin = getattr(spec, "origin", None)
                    if origin and origin != "built-in":
                        return str(Path(origin))
                    search = getattr(spec, "submodule_search_locations", None)
                    if search:
                        try:
                            return str(Path(list(search)[0]))
                        except Exception:
                            pass
                return mod.__name__
            return ""

        # YAML agent
        doc = self.yaml_document
        if doc is not None:
            for attr in ("path", "file_path", "source_path", "uri", "url"):
                val = getattr(doc, attr, None)
                if val:
                    return str(val)
        return ""
