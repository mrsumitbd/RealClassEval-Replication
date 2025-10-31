
from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional

# Forward declaration for type checking – the real class is defined elsewhere


class YamlAgentDocument:  # pragma: no cover
    path: str


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Optional[Path] = None,
        module: Optional[ModuleType] = None,
        yaml_document: Optional[YamlAgentDocument] = None,
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

        # Basic validation – at least one definition source must be provided
        if not (self._file_path or self._module or self._yaml_document):
            raise ValueError(
                "At least one of file_path, module, or yaml_document must be provided")

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        if self._module is not None:
            return 'python'
        if self._yaml_document is not None:
            return 'yaml'
        # Fallback: if only file_path is provided, infer from extension
        if self._file_path is not None:
            ext = self._file_path.suffix.lower()
            if ext in {'.py'}:
                return 'python'
            if ext in {'.yaml', '.yml'}:
                return 'yaml'
        raise RuntimeError("Unable to determine agent kind")

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self._file_path is not None:
            return str(self._file_path.resolve())
        if self._module is not None:
            # Prefer __file__ if available, otherwise use spec.origin
            return getattr(self._module, '__file__', getattr(self._module, '__spec__', None).origin)
        if self._yaml_document is not None:
            return getattr(self._yaml_document, 'path', '')
        raise RuntimeError("No path available for agent")
