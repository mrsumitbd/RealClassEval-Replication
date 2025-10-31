
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional, Set


@dataclass
class SearchResult:
    """Dataclass to hold search results."""

    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line: Optional[int] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root."""
        return os.path.relpath(file_path, start=project_root)

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Return a tagged string containing only the file path."""
        rel = self.to_relative_path(self.file_path, project_root)
        return f"{rel}"

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Convert the search result to a tagged string, up to class."""
        rel = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            return f"{rel}::{self.class_name}"
        return rel

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Convert the search result to a tagged string, up to function."""
        rel = self.to_relative_path(self.file_path, project_root)
        parts = [rel]
        if self.class_name:
            parts.append(self.class_name)
        if self.func_name:
            parts.append(self.func_name)
        return "::".join(parts)

    def to_tagged_str(self, project_root: str) -> str:
        """Return a fully tagged string including line number if available."""
        base = self.to_tagged_upto_func(project_root)
        if self.line is not None:
            return f"{base}:{self.line}"
        return base

    @staticmethod
    def collapse_to_file_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse a list of SearchResult objects to unique file-level tags."""
        seen: Set[str] = set()
        lines: List[str] = []
        for sr in lst:
            tag = sr.to_tagged_upto_file(project_root)
            if tag not in seen:
                seen.add(tag)
                lines.append(tag)
        return "\n".join(lines)

    @staticmethod
    def collapse_to_method_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse a list of SearchResult objects to unique method-level tags."""
        seen: Set[str] = set()
        lines: List[str] = []
        for sr in lst:
            tag = sr.to_tagged_upto_func(project_root)
            if tag not in seen:
                seen.add(tag)
                lines.append(tag)
        return "\n".join(lines)
