
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional


class YamlAgentDocument:
    # Assuming YamlAgentDocument is defined elsewhere
    pass


class AgentInfo:

    def __init__(self, name: str, description: str, file_path: Optional[Path] = None, module: Optional[ModuleType] = None, yaml_document: Optional[YamlAgentDocument] = None) -> None:
        self.name = name
        self.description = description
        self.file_path = file_path
        self.module = module
        self.yaml_document = yaml_document

        if (self.file_path is None and self.module is None and self.yaml_document is None) or \
           (self.file_path is not None and (self.module is not None or self.yaml_document is not None)) or \
           (self.module is not None and (self.file_path is not None or self.yaml_document is not None)) or \
           (self.yaml_document is not None and (self.file_path is not None or self.module is not None)):
            raise ValueError(
                "Exactly one of file_path, module, or yaml_document must be provided")

    @property
    def kind(self) -> Literal['python', 'yaml']:
        if self.module is not None:
            return 'python'
        elif self.yaml_document is not None:
            return 'yaml'
        else:
            raise ValueError("Unable to determine kind")

    @property
    def path(self) -> str:
        if self.file_path is not None:
            return str(self.file_path)
        elif self.module is not None:
            return self.module.__file__ or ''
        else:
            raise ValueError("Path is not available for yaml agents")
