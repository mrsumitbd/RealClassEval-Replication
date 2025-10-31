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
        if not name:
            raise ValueError("name must be a non-empty string")

        if (module is None and yaml_document is None) or (
            module is not None and yaml_document is not None
        ):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided")

        self.name = name
        self.description = description
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document
        self._kind: Literal["python",
                            "yaml"] = "python" if module is not None else "yaml"

    @property
    def kind(self) -> Literal["python", "yaml"]:
        """Get the definition type of the agent."""
        return self._kind

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self._file_path is not None:
            return str(self._file_path)

        if self._kind == "python":
            mod = self._module
            if mod is not None:
                mod_file = getattr(mod, "__file__", None)
                if mod_file:
                    return str(mod_file)
                mod_path = getattr(mod, "__path__", None)
                if mod_path:
                    try:
                        return str(next(iter(mod_path)))
                    except StopIteration:
                        pass
            return ""
        else:
            doc = self._yaml_document
            if doc is not None:
                candidate = getattr(doc, "path", None)
                if candidate is None:
                    candidate = getattr(doc, "file_path", None)
                if candidate is None:
                    candidate = getattr(doc, "source", None)
                if candidate is None:
                    candidate = getattr(doc, "uri", None)
                return str(candidate) if candidate is not None else ""
            return ""
