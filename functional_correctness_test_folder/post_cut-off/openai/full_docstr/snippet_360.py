
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Iterable


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    line: int
    column: int = 0
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    snippet: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root."""
        return str(Path(file_path).relative_to(Path(project_root)))

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto file path."""
        rel = self.to_relative_path(self.file_path, project_root)
        return f"{rel}:{self.line}"

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto class."""
        rel = self.to_relative_path(self.file_path, project_root)
        cls = self.class_name or ""
        return f"{rel}:{self.line}:{cls}"

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto function."""
        rel = self.to_relative_path(self.file_path, project_root)
        cls = self.class_name or ""
        func = self.func_name or ""
        return f"{rel}:{self.line}:{cls}:{func}"

    def to_tagged_str(self, project_root: str) -> str:
        """Convert the search result to a fully tagged string."""
        rel = self.to_relative_path(self.file_path, project_root)
        cls = self.class_name or ""
        func = self.func_name or ""
        snip = self.snippet or ""
        return f"{rel}:{self.line}:{self.column}:{cls}:{func}:{snip}"

    @staticmethod
    def collapse_to_file_level(
        lst: Iterable["SearchResult"], project_root: str
    ) -> str:
        """Collapse search results to file level."""
        files = {sr.to_relative_path(sr.file_path, project_root) for sr in lst}
        return "\n".join(sorted(files))

    @staticmethod
    def collapse_to_method_level(
        lst: Iterable["SearchResult"], project_root: str
    ) -> str:
        """Collapse search results to method level."""
        methods = {
            sr.to_tagged_upto_func(project_root) for sr in lst
        }
        return "\n".join(sorted(methods))
