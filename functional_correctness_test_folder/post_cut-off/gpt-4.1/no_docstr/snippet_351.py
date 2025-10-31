
from pathlib import Path
from types import ModuleType
from typing import Literal


class YamlAgentDocument:
    pass  # Placeholder for type hinting


class AgentInfo:

    def __init__(
        self,
        name: str,
        description: str,
        file_path: Path | None = None,
        module: 'ModuleType | None' = None,
        yaml_document: 'YamlAgentDocument | None' = None
    ) -> None:
        self.name = name
        self.description = description
        self.file_path = file_path
        self.module = module
        self.yaml_document = yaml_document

    @property
    def kind(self) -> Literal['python', 'yaml']:
        if self.module is not None:
            return 'python'
        elif self.yaml_document is not None:
            return 'yaml'
        else:
            raise ValueError(
                "AgentInfo must have either a module or a yaml_document.")

    @property
    def path(self) -> str:
        if self.file_path is not None:
            return str(self.file_path)
        elif self.module is not None and hasattr(self.module, '__file__') and self.module.__file__:
            return str(self.module.__file__)
        else:
            return ""
