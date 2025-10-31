
from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Any


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Path | None = None,
        module: ModuleType | None = None,
        yaml_document: Any | None = None,
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

        # Basic validation: at least one of module or yaml_document must be provided
        if self._module is None and self._yaml_document is None:
            raise ValueError(
                "Either 'module' or 'yaml_document' must be provided")

        # If both are provided, prefer module (Python agent)
        if self._module is not None and self._yaml_document is not None:
            # Warn or ignore yaml_document
            pass

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        if self._module is not None:
            return 'python'
        if self._yaml_document is not None:
            return 'yaml'
        raise ValueError("Agent kind cannot be determined")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        # Prefer explicit file_path
        if self._file_path is not None:
            return str(self._file_path)

        # If module is available, use its __file__ attribute
        if self._module is not None:
            module_file = getattr(self._module, "__file__", None)
            if module_file:
                return str(module_file)

        # If yaml_document has a path attribute, use it
        if self._yaml_document is not None:
            yaml_path = getattr(self._yaml_document, "path", None)
            if yaml_path:
                return str(yaml_path)

        raise ValueError("Cannot determine path for the agent")
