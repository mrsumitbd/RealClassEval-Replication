from pathlib import Path
from types import ModuleType
from typing import Literal


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
        if not name:
            raise ValueError("name must be a non-empty string")
        if module is not None and yaml_document is not None:
            raise ValueError(
                "Specify either module or yaml_document, not both")
        if module is None and yaml_document is None:
            raise ValueError("Either module or yaml_document must be provided")

        self.name = name
        self.description = description
        self._module = module
        self._yaml_document = yaml_document

        if module is not None:
            self._kind: Literal['python', 'yaml'] = 'python'
        else:
            self._kind = 'yaml'

        # Determine path
        resolved_path: str | None = None
        if file_path is not None:
            try:
                resolved_path = str(file_path.resolve())
            except Exception:
                resolved_path = str(file_path)

        if resolved_path is None:
            if self._kind == 'python' and module is not None:
                mod_file = getattr(module, '__file__', None)
                if isinstance(mod_file, str):
                    resolved_path = mod_file
                else:
                    mod_path = getattr(module, '__path__', None)
                    if mod_path:
                        try:
                            # __path__ can be a listlike; get first element
                            first = next(iter(mod_path))
                            resolved_path = str(first)
                        except Exception:
                            resolved_path = module.__name__
                    else:
                        resolved_path = module.__name__
            else:
                # Try to extract path-like attribute from yaml_document
                yd = yaml_document
                candidate = None
                for attr in ('path', 'file_path', 'source_path', 'filepath'):
                    candidate = getattr(
                        yd, attr, None) if yd is not None else None
                    if candidate:
                        break
                if isinstance(candidate, Path):
                    try:
                        resolved_path = str(candidate.resolve())
                    except Exception:
                        resolved_path = str(candidate)
                elif isinstance(candidate, str):
                    resolved_path = candidate
                else:
                    resolved_path = ''

        self._path = resolved_path

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        return self._kind

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        return self._path
