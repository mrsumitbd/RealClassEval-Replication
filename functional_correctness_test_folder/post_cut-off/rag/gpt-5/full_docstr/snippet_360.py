from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple, Union
import os


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line_no: Optional[int] = None
    col_no: Optional[int] = None
    snippet: Optional[str] = None
    score: Optional[float] = None
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        # Normalize empty strings to None
        if self.class_name == "":
            self.class_name = None
        if self.func_name == "":
            self.func_name = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        """
        if not file_path:
            return ""
        # Normalize inputs
        file_path = os.path.abspath(file_path)
        root = os.path.abspath(project_root) if project_root else os.getcwd()
        try:
            rel = os.path.relpath(file_path, root)
        except ValueError:
            # On Windows, drives might differ; fall back to absolute path
            rel = file_path
        # Use POSIX-style separators for consistency
        return rel.replace("\\", "/")

    def _tag_parts_upto_file(self, project_root: str) -> Tuple[str]:
        rel = self.to_relative_path(self.file_path, project_root)
        return (f"file:{rel}",)

    def _tag_parts_upto_class(self, project_root: str) -> Tuple[str, ...]:
        parts = list(self._tag_parts_upto_file(project_root))
        if self.class_name:
            parts.append(f"class:{self.class_name}")
        return tuple(parts)

    def _tag_parts_upto_func(self, project_root: str) -> Tuple[str, ...]:
        parts = list(self._tag_parts_upto_class(project_root))
        if self.func_name:
            parts.append(f"func:{self.func_name}")
        return tuple(parts)

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto file path."""
        return " | ".join(self._tag_parts_upto_file(project_root))

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto class."""
        parts = self._tag_parts_upto_class(project_root)
        return " | ".join(parts)

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto function."""
        parts = self._tag_parts_upto_func(project_root)
        return " | ".join(parts)

    def to_tagged_str(self, project_root: str) -> str:
        """Convert the search result to a tagged string."""
        parts = list(self._tag_parts_upto_func(project_root))
        if self.line_no is not None:
            parts.append(f"line:{self.line_no}")
        if self.col_no is not None:
            parts.append(f"col:{self.col_no}")
        if self.score is not None:
            parts.append(f"score:{self.score:.4f}")
        return " | ".join(parts)

    @staticmethod
    def _to_search_result(item: Union["SearchResult", dict]) -> "SearchResult":
        if isinstance(item, SearchResult):
            return item
        if isinstance(item, dict):
            return SearchResult(
                file_path=item.get("file_path") or item.get("path") or "",
                class_name=item.get("class_name"),
                func_name=item.get("func_name") or item.get("function"),
                line_no=item.get("line_no") or item.get("line"),
                col_no=item.get("col_no") or item.get("column"),
                snippet=item.get("snippet"),
                score=item.get("score"),
                meta=item.get("meta") or {},
            )
        raise TypeError(
            "Unsupported item type for collapse: expected SearchResult or dict")

    @staticmethod
    def collapse_to_file_level(lst: Iterable[Union["SearchResult", dict]], project_root: str) -> str:
        """Collapse search results to file level."""
        seen = {}
        for item in lst:
            sr = SearchResult._to_search_result(item)
            tag = sr.to_tagged_upto_file(project_root)
            if tag not in seen:
                seen[tag] = None
        return "\n".join(seen.keys())

    @staticmethod
    def collapse_to_method_level(lst: Iterable[Union["SearchResult", dict]], project_root: str) -> str:
        """Collapse search results to method level."""
        seen = {}
        for item in lst:
            sr = SearchResult._to_search_result(item)
            tag = sr.to_tagged_upto_func(project_root)
            if tag not in seen:
                seen[tag] = None
        return "\n".join(seen.keys())
