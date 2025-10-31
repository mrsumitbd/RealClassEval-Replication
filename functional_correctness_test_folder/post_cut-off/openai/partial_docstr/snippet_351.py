
from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # The actual YamlAgentDocument type is defined elsewhere in the project.
    # Import it only for type checking to avoid circular imports at runtime.
    from .yaml_agent_document import YamlAgentDocument  # pragma: no cover
else:
    YamlAgentDocument = object  # fallback placeholder


class AgentInfo:
    """Agent information container supporting both Python and YAML agents."""

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Optional[Path] = None,
        module: Optional[ModuleType] = None,
        yaml_document: Optional[YamlAgentDocument] = None,
    ) -> None:
        if module is None and yaml_document is None:
            raise ValueError(
                "Either `module` or `yaml_document` must be provided.")
        if module is not None and yaml_document is not None:
            # Prefer the explicit file_path if both are given
            if file_path is None:
                # If a module is provided, we can derive a path from it
                file_path = Path(getattr(module, "__file__", ""))

        self.name = name
        self.description = description
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Get the definition type of the agent."""
        return "python" if self._module is not None else "yaml"

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self._file_path is not None:
            return str(self._file_path)
        if self._module is not None:
            return getattr(self._module, "__file__", "")
        if self._yaml_document is not None:
            # Assume the YAML document exposes a `path` attribute
            return getattr(self._yaml_document, "path", "")
        return ""
