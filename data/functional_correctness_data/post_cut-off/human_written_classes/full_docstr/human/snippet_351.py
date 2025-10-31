from typing import TYPE_CHECKING, Literal
from pathlib import Path

class AgentInfo:
    """Agent information container supporting both Python and YAML agents."""

    def __init__(self, name: str, description: str, file_path: Path | None=None, module: 'ModuleType | None'=None, yaml_document: 'YamlAgentDocument | None'=None) -> None:
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
        if self.yaml_document is not None:
            return 'yaml'
        if self.module is not None:
            return 'python'
        msg = f'Agent {self.name} is not a Python or YAML agent'
        raise ValueError(msg)

    @property
    def path(self) -> str:
        """Get the definition path of the agent."""
        if self.file_path:
            return str(self.file_path)
        if self.module and self.module.__file__:
            return self.module.__file__
        msg = f'Agent {self.name} definition path is unknown'
        raise ValueError(msg)