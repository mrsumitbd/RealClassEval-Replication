from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Literal, Optional


class AgentInfo:
    def __init__(
        self,
        name: str,
        description: str,
        file_path: Optional[Path] = None,
        module: Optional[ModuleType] = None,
        yaml_document: Optional["YamlAgentDocument"] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.file_path = file_path
        self.module = module
        self.yaml_document = yaml_document

    @property
    def kind(self) -> Literal["python", "yaml"]:
        if self.yaml_document is not None:
            return "yaml"
        if self.module is not None:
            return "python"
        if isinstance(self.file_path, Path):
            suffix = self.file_path.suffix.lower()
            if suffix in {".yaml", ".yml"}:
                return "yaml"
            if suffix == ".py":
                return "python"
        return "python"

    @property
    def path(self) -> str:
        if self.file_path is not None:
            return str(self.file_path)

        if self.kind == "yaml" and self.yaml_document is not None:
            p = getattr(self.yaml_document, "file_path", None) or getattr(
                self.yaml_document, "path", None
            )
            if isinstance(p, Path):
                return str(p)
            if isinstance(p, str):
                return p

        if self.kind == "python" and self.module is not None:
            mod_file = getattr(self.module, "__file__", None)
            if isinstance(mod_file, str):
                return mod_file
            spec = getattr(self.module, "__spec__", None)
            origin = getattr(
                spec, "origin", None) if spec is not None else None
            if isinstance(origin, str):
                return origin

        return ""
