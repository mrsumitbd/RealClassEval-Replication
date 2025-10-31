
from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional

# Forward declaration for type checking
try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from yaml_agent_document import YamlAgentDocument  # type: ignore
except Exception:
    YamlAgentDocument = None  # pragma: no cover


class AgentInfo:
    """
    Holds metadata about an agent implementation.

    Parameters
    ----------
    name : str
        The name of the agent.
    description : str
        A short description of the agent.
    file_path : Path | None, optional
        Path to the file that defines the agent.  If omitted, the path will be
        inferred from ``module`` or ``yaml_document``.
    module : ModuleType | None, optional
        The Python module that implements the agent.  Mutually exclusive with
        ``yaml_document``.
    yaml_document : YamlAgentDocument | None, optional
        The YAML document that defines the agent.  Mutually exclusive with
        ``module``.
    """

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Optional[Path] = None,
        module: Optional[ModuleType] = None,
        yaml_document: Optional["YamlAgentDocument"] = None,
    ) -> None:
        self.name = name
        self.description = description
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document

        # Basic validation
        if module is not None and yaml_document is not None:
            raise ValueError(
                "Only one of 'module' or 'yaml_document' may be provided.")
        if module is None and yaml_document is None:
            raise ValueError(
                "Either 'module' or 'yaml_document' must be provided.")

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Return the kind of agent implementation."""
        if self._module is not None:
            return "python"
        if self._yaml_document is not None:
            return "yaml"
        # This should never happen due to validation in __init__
        raise RuntimeError("AgentInfo is in an invalid state.")

    @property
    def path(self) -> str:
        """Return the file path of the agent implementation."""
        if self._file_path is not None:
            return str(self._file_path)

        if self._module is not None:
            return getattr(self._module, "__file__", "")

        if self._yaml_document is not None:
            # Try common attribute names that a YAML document might expose
            return getattr(
                self._yaml_document,
                "file_path",
                getattr(self._yaml_document, "path", ""),
            )

        # Fallback: empty string
        return ""
