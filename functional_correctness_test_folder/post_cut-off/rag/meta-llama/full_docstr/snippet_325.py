
from pathlib import Path
from typing import Literal, Optional
from types import ModuleType


class YamlAgentDocument:  # Assuming this class exists
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

    @property
    def kind(self) -> Literal['python', 'yaml']:
        """Get the definition type of the agent."""
        if self.module is not None:
            return 'python'
        elif self.yaml_document is not None:
            return 'yaml'
        else:
            raise ValueError("Agent type could not be determined")

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self.kind == 'python':
            if self.module is None or not hasattr(self.module, '__file__'):
                raise ValueError("Python agent module has no file attribute")
            return self.module.__file__
        elif self.kind == 'yaml':
            if self.file_path is None:
                raise ValueError("YAML agent file path is not set")
            return str(self.file_path)
        else:
            raise ValueError("Agent type is not supported")
