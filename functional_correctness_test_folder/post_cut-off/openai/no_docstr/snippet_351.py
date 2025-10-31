
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
    """
    Holds metadata about an agent implementation.

    Parameters
    ----------
    name : str
        The name of the agent.
    description : str
        A short description of the agent.
    file_path : Path | None, optional
        Explicit file path to the agent source. If omitted, the path will be
        inferred from the module or yaml_document.
    module : ModuleType | None, optional
        The imported Python module that implements the agent.
    yaml_document : YamlAgentDocument | None, optional
        The parsed YAML document that defines the agent.
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
        self.module = module
        self.yaml_document = yaml_document

        # Basic validation: at least one of module or yaml_document must be provided
        if self.module is None and self.yaml_document is None:
            raise ValueError("Either module or yaml_document must be provided")

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Return the kind of agent implementation."""
        if self.module is not None:
            return "python"
        if self.yaml_document is not None:
            return "yaml"
        # This should never happen due to validation in __init__
        raise RuntimeError("AgentInfo has no valid implementation source")

    @property
    def path(self) -> str:
        """Return the file path of the agent source as a string."""
        # Prefer explicit file_path if provided
        if self._file_path is not None:
            return str(self._file_path)

        # Infer from module
        if self.module is not None:
            module_file = getattr(self.module, "__file__", None)
            if module_file:
                return str(module_file)

        # Infer from yaml_document
        if self.yaml_document is not None:
            # Assume YamlAgentDocument has a `path` attribute
            yaml_path = getattr(self.yaml_document, "path", None)
            if yaml_path:
                return str(yaml_path)

        # Fallback: raise an error
        raise RuntimeError("Unable to determine the path for the agent")
