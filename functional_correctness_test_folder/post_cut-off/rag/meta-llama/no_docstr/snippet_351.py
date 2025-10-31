
from pathlib import Path
from typing import Literal, Optional
from types import ModuleType


class YamlAgentDocument:  # Assuming this class is defined elsewhere
    pass


class AgentInfo:
    """Agent information container supporting both Python and YAML agents."""

    def __init__(self, name: str, description: str, file_path: Optional[Path] = None, module: Optional[ModuleType] = None, yaml_document: Optional[YamlAgentDocument] = None) -> None:
        """Initialize agent info.

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

        if (module is not None and yaml_document is not None) or (module is None and yaml_document is None):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided")

    @property
    def kind(self) -> Literal['python', 'yaml']:
        """Get the definition type of the agent."""
        if self.module is not None:
            return 'python'
        else:
            return 'yaml'

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self.kind == 'python':
            if self.module is None:
                raise ValueError("Module is not set for this agent")
            return self.module.__file__  # type: ignore
        else:
            if self.file_path is None:
                raise ValueError("File path is not set for this agent")
            return str(self.file_path)
