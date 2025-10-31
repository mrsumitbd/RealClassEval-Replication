from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from typing import Any

    class YamlAgentDocument:
        ...  # Placeholder for type checking


class AgentInfo:

    def __init__(self, name: str, description: str, file_path: Path | None = None, module: ModuleType | None = None, yaml_document: 'YamlAgentDocument | None' = None) -> None:
        '''Initialize agent info.
        Args:
            name: Agent name
            description: Agent description
            file_path: Path to agent file/directory
            module: Python module (for Python agents)
            yaml_document: YAML agent document (for YAML agents)
        '''
        self.name: str = name
        self.description: str = description
        self.file_path: Optional[Path] = file_path
        self.module: Optional[ModuleType] = module
        self.yaml_document: Optional['YamlAgentDocument'] = yaml_document

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        if self.module is not None:
            return 'python'
        if self.yaml_document is not None:
            return 'yaml'
        if self.file_path is not None:
            suf = self.file_path.suffix.lower()
            if suf in ('.py', '.pyc', '.pyo'):
                return 'python'
            if suf in ('.yaml', '.yml'):
                return 'yaml'
        return 'python'

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)

        if self.module is not None:
            mfile = getattr(self.module, '__file__', None)
            if mfile:
                return str(mfile)

        ydoc = self.yaml_document
        if ydoc is not None:
            for attr in ('file_path', 'path', 'source_path', 'source', 'location'):
                p = getattr(ydoc, attr, None)
                if p:
                    return str(p)

        return ''
