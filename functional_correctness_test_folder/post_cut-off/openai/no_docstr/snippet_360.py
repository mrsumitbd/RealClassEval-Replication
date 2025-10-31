
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SearchResult:
    file_path: str
    line: Optional[int] = None
    column: Optional[int] = None
    class_name: Optional[str] = None
    func_name: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Return the path of *file_path* relative to *project_root*."""
        return os.path.relpath(file_path, start=project_root)

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Return a tag that includes the file and line number."""
        rel = self.to_relative_path(self.file_path, project_root)
        if self.line is not None:
            return f"{rel}:{self.line}"
        return rel

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Return a tag that includes the file, class name and line number."""
        base = self.to_tagged_upto_file(project_root)
        if self.class_name:
            return f"{base}:{self.class_name}"
        return base

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Return a tag that includes the file, class name, function name and line number."""
        base = self.to_tagged_upto_class(project_root)
        if self.func_name:
            return f"{base}:{self.func_name}"
        return base

    def to_tagged_str(self, project_root: str) -> str:
        """Return a fully-qualified tag including file, class, function, line and column."""
        tag = self.to_tagged_upto_func(project_root)
        if self.line is not None:
            tag += f":{self.line}"
        if self.column is not None:
            tag += f":{self.column}"
        return tag

    @staticmethod
    def collapse_to_file_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse a list of SearchResult objects to a comma‑separated string of unique file tags."""
        tags = {sr.to_tagged_upto_file(project_root) for sr in lst}
        return ", ".join(sorted(tags))

    @staticmethod
    def collapse_to_method_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse a list of SearchResult objects to a comma‑separated string of unique method tags."""
        tags = {sr.to_tagged_upto_func(project_root) for sr in lst}
        return ", ".join(sorted(tags))
