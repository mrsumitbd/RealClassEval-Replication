
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Iterable, Set


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    line: int = 0
    class_name: Optional[str] = None
    function_name: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root."""
        return str(Path(file_path).resolve().relative_to(Path(project_root).resolve()))

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto file path."""
        rel = self.to_relative_path(self.file_path, project_root)
        return f"{rel}:{self.line}"

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto class."""
        rel = self.to_relative_path(self.file_path, project_root)
        cls = self.class_name or ""
        return f"{rel}:{cls}:{self.line}"

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto function."""
        rel = self.to_relative_path(self.file_path, project_root)
        cls = self.class_name or ""
        func = self.function_name or ""
        return f"{rel}:{cls}:{func}:{self.line}"

    def to_tagged_str(self, project_root: str) -> str:
        """Convert the search result to a tagged string."""
        return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        """Collapse search results to file level."""
        unique: Set[str] = set()
        for sr in lst:
            unique.add(sr.to_tagged_upto_file(project_root))
        return "\n".join(sorted(unique))

    @staticmethod
    def collapse_to_method_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        """Collapse search results to method level."""
        unique: Set[str] = set()
        for sr in lst:
            unique.add(sr.to_tagged_upto_func(project_root))
        return "\n".join(sorted(unique))
