
import os
from dataclasses import dataclass
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
        """Convert the search result to a tagged string, up to file path."""
        rel = self.to_relative_path(self.file_path, project_root)
        return rel

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
        """Convert the search result to a tagged string."""
        return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse search results to file level."""
        unique_files: Set[str] = set()
        for res in lst:
            unique_files.add(res.to_tagged_upto_file(project_root))
        return "\n".join(sorted(unique_files))

    @staticmethod
    def collapse_to_method_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse search results to method level."""
        unique_methods: Set[str] = set()
        for res in lst:
            unique_methods.add(res.to_tagged_upto_func(project_root))
        return "\n".join(sorted(unique_methods))
