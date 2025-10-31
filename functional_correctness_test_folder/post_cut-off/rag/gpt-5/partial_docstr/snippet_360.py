from dataclasses import dataclass
from typing import Optional, Iterable
import os


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    line_no: Optional[int] = None
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    snippet: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        """
        try:
            # Handle both absolute and relative inputs robustly
            return os.path.relpath(file_path, start=project_root)
        except Exception:
            return file_path

    def _base_tag(self, project_root: str) -> str:
        rel = self.to_relative_path(self.file_path, project_root)
        return f"[FILE] {rel}"

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto file path."""
        return self._base_tag(project_root)

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto class."""
        s = self._base_tag(project_root)
        if self.class_name:
            s += f" [CLASS] {self.class_name}"
        return s

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto function."""
        s = self.to_tagged_upto_class(project_root)
        if self.func_name:
            s += f" [FUNC] {self.func_name}"
        return s

    def to_tagged_str(self, project_root: str) -> str:
        """Convert the search result to a tagged string."""
        s = self.to_tagged_upto_func(project_root)
        if self.line_no is not None:
            s += f" [LINE] {self.line_no}"
        if self.snippet:
            snippet = self.snippet.strip()
            if snippet:
                s += f" — {snippet}"
        return s

    @staticmethod
    def collapse_to_file_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        """Collapse search results to file level."""
        unique = set()
        for item in lst:
            if isinstance(item, SearchResult):
                unique.add(item.to_tagged_upto_file(project_root))
            else:
                # Fallback in case of unexpected item types
                unique.add(str(item))
        return "\n".join(sorted(unique))

    @staticmethod
    def collapse_to_method_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        """Collapse search results to method level."""
        unique = set()
        for item in lst:
            if isinstance(item, SearchResult):
                unique.add(item.to_tagged_upto_func(project_root))
            else:
                unique.add(str(item))
        return "\n".join(sorted(unique))
