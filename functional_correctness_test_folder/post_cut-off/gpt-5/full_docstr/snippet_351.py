from typing import Literal, Optional
from types import ModuleType
from pathlib import Path


class AgentInfo:
    '''Agent information container supporting both Python and YAML agents.'''

    def __init__(self, name: str, description: str, file_path: Path | None = None, module: 'ModuleType | None' = None, yaml_document: 'YamlAgentDocument | None' = None) -> None:
        '''Initialize agent info.
        Args:
            name: Agent name
            description: Agent description
            file_path: Path to agent file/directory
            module: Python module (for Python agents)
            yaml_document: YAML agent document (for YAML agents)
        '''
        if (module is None) == (yaml_document is None):
            raise ValueError(
                "Exactly one of 'module' or 'yaml_document' must be provided.")
        self._name: str = name
        self._description: str = description
        self._file_path: Optional[Path] = file_path
        self._module: Optional[ModuleType] = module
        self._yaml_document = yaml_document

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        return 'python' if self._module is not None else 'yaml'

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self._file_path is not None:
            return str(self._file_path)

        if self._module is not None:
            mod = self._module
            file_attr = getattr(mod, '__file__', None)
            if file_attr:
                return str(file_attr)
            path_attr = getattr(mod, '__path__', None)
            if path_attr:
                try:
                    return str(path_attr[0])
                except Exception:
                    pass
            return ''

        doc = self._yaml_document
        if doc is not None:
            for attr in ('file_path', 'path', 'source', 'uri'):
                value = getattr(doc, attr, None)
                if value:
                    try:
                        return str(value)
                    except Exception:
                        continue
        return ''
