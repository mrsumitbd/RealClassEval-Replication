from __future__ import annotations

from pathlib import Path
from typing import Literal
from types import ModuleType


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(self, name: str, description: str, file_path: Path | None = None, module: 'ModuleType | None' = None, yaml_document: 'YamlAgentDocument | None' = None) -> None:
        if module is not None and yaml_document is not None:
            raise ValueError(
                "Specify either 'module' for Python agents or 'yaml_document' for YAML agents, not both.")

        self.name = name
        self.description = description
        self.module = module
        self.yaml_document = yaml_document
        self.file_path = file_path

        if yaml_document is not None:
            self._kind: Literal['python', 'yaml'] = 'yaml'
        else:
            self._kind = 'python'

        resolved_path: str | None = None
        if self.file_path is not None:
            resolved_path = str(self.file_path)
        elif self.yaml_document is not None:
            # Try common attributes to extract path from the YAML document
            for attr in ('path', 'file_path', 'filepath', 'source_path'):
                p = getattr(self.yaml_document, attr, None)
                if p:
                    resolved_path = str(p)
                    break
        elif self.module is not None:
            resolved_path = getattr(self.module, '__file__', None)

        self._path = resolved_path or ""

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        return self._kind

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        return self._path
