
from pathlib import Path
from typing import Literal, Optional
import types


class AgentInfo:

    def __init__(self, name: str, description: str, file_path: Optional[Path] = None, module: Optional[types.ModuleType] = None, yaml_document: Optional['YamlAgentDocument'] = None) -> None:
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
                "AgentInfo must have either a module or a yaml_document")

    @property
    def path(self) -> str:
        if self.file_path:
            return str(self.file_path)
        else:
            raise ValueError("AgentInfo does not have a file path")
