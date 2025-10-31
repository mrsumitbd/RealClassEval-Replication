from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Optional[Path] = None,
        module: Optional[ModuleType] = None,
        yaml_document: Optional["YamlAgentDocument"] = None,
    ) -> None:
        '''Initialize agent info.
        Args:
            name: Agent name
            description: Agent description
            file_path: Path to agent file/directory
            module: Python module (for Python agents)
            yaml_document: YAML agent document (for YAML agents)
        '''
        self.name = name
        self.description = description
        self._file_path = file_path
        self._module = module
        self._yaml_document = yaml_document

        if self._module is None and self._yaml_document is None:
            raise ValueError(
                "Either a Python module or a YAML document must be provided.")
        if self._module is not None and self._yaml_document is not None:
            raise ValueError(
                "Only one of module or yaml_document should be provided.")

    @property
    def kind(self) -> Literal["python", "yaml"]:
        '''Get the definition type of the agent.'''
        if self._module is not None:
            return "python"
        if self._yaml_document is not None:
            return "yaml"
        raise RuntimeError(
            "AgentInfo is in an invalid state: no definition provided.")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.kind == "python":
            if self._module is not None and hasattr(self._module, "__file__"):
                return str(self._module.__file__)
            if self._file_path is not None:
                return str(self._file_path)
            raise RuntimeError("Python agent has no file path.")
        if self.kind == "yaml":
            if hasattr(self._yaml_document, "path"):
                return str(self._yaml_document.path)
            raise RuntimeError("YAML agent document has no path attribute.")
        raise RuntimeError("AgentInfo is in an invalid state: unknown kind.")
