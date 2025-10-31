from pathlib import Path
from typing import Literal
from types import ModuleType
import inspect


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
        self.name = name
        self.description = description
        self.file_path = Path(file_path) if file_path is not None else None
        self.module = module
        self.yaml_document = yaml_document

        if self.module is not None and self.yaml_document is not None:
            raise ValueError('agent cannot be both python and yaml')

        # Determine kind if not explicitly inferable
        self._kind: Literal['python', 'yaml'] | None = None
        if self.module is not None:
            self._kind = 'python'
        elif self.yaml_document is not None:
            self._kind = 'yaml'
        elif self.file_path is not None:
            suffix = self.file_path.suffix.lower()
            if suffix in ('.yaml', '.yml'):
                self._kind = 'yaml'
            else:
                self._kind = 'python'
        else:
            raise ValueError(
                'insufficient information to determine agent kind')

    @property
    def kind(self) -> Literal['python', 'yaml']:
        '''Get the definition type of the agent.'''
        # _kind is always set in __init__
        return self._kind  # type: ignore[return-value]

    @property
    def path(self) -> str:
        '''Get the definition path of the agent.'''
        if self.file_path is not None:
            return str(self.file_path)

        if self.module is not None:
            mod_file = getattr(self.module, '__file__', None)
            if isinstance(mod_file, str):
                return mod_file
            # Fallbacks to try to determine module location
            try:
                return inspect.getfile(self.module)  # type: ignore[arg-type]
            except Exception:
                spec = getattr(self.module, '__spec__', None)
                origin = getattr(
                    spec, 'origin', None) if spec is not None else None
                if isinstance(origin, str):
                    return origin
            return ''

        if self.yaml_document is not None:
            for attr in ('file_path', 'path', 'source', 'location'):
                val = getattr(self.yaml_document, attr, None)
                if val is not None:
                    return str(val)
            return ''

        return ''
