from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line_no: Optional[int] = None
    col: Optional[int] = None
    score: Optional[float] = None
    summary: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        """
        file_p = Path(file_path).resolve()
        root_p = Path(project_root).resolve()
        try:
            rel = file_p.relative_to(root_p)
        except Exception:
            # Fall back to a best-effort relative path
            try:
                rel = Path(Path(file_p).as_posix().replace(
                    root_p.as_posix().rstrip('/') + '/', ''))
            except Exception:
                rel = file_p
        return rel.as_posix()

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto file path."""
        rel = self.to_relative_path(self.file_path, project_root)
        return f"[FILE] {rel}"

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto class."""
        base = self.to_tagged_upto_file(project_root)
        if self.class_name:
            return f"{base} [CLASS] {self.class_name}"
        return base

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Convert the search result to a tagged string, upto function."""
        base = self.to_tagged_upto_class(project_root)
        if self.func_name:
            return f"{base} [FUNC] {self.func_name}"
        return base

    def to_tagged_str(self, project_root: str) -> str:
        """Convert the search result to a tagged string."""
        base = self.to_tagged_upto_func(project_root)
        parts = [base]
        if self.line_no is not None:
            parts.append(f"[LINE] {self.line_no}")
        if self.col is not None:
            parts.append(f"[COL] {self.col}")
        return " ".join(parts)

    @staticmethod
    def collapse_to_file_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        """Collapse search results to file level."""
        unique = {item.to_tagged_upto_file(project_root) for item in lst}
        return "\n".join(sorted(unique))

    @staticmethod
    def collapse_to_method_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        """Collapse search results to method level."""
        unique = {item.to_tagged_upto_func(project_root) for item in lst}
        return "\n".join(sorted(unique))
