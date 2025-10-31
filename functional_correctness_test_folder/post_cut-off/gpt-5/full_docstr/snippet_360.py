from dataclasses import dataclass
from typing import List, Optional, Iterable, Tuple
from pathlib import Path
import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line: Optional[int] = None
    col: Optional[int] = None
    preview: Optional[str] = None
    score: Optional[float] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        '''
        if not file_path:
            return file_path
        try:
            file_p = Path(file_path).expanduser()
            root_p = Path(project_root).expanduser()
            # Resolve as much as possible without requiring that the path exists
            try:
                file_abs = file_p if file_p.is_absolute() else (root_p / file_p).resolve()
            except Exception:
                file_abs = file_p if file_p.is_absolute() else (root_p / file_p)
            try:
                root_abs = root_p.resolve()
            except Exception:
                root_abs = root_p

            # If file is within project root, return a relative path; else return original string
            try:
                common = os.path.commonpath([str(file_abs), str(root_abs)])
            except Exception:
                # If drives differ on Windows or invalid input, fall back
                common = ""

            if common and os.path.samefile(common, str(root_abs)) if Path(common).exists() and Path(root_abs).exists() else str(common) == str(root_abs):
                try:
                    return os.path.relpath(str(file_abs), str(root_abs))
                except Exception:
                    return str(file_p)
            else:
                # If already relative, return as-is
                return str(file_p) if not file_p.is_absolute() else str(file_p)
        except Exception:
            return file_path

    def _tag_components(self, project_root: str, upto: str = "all") -> List[str]:
        rel = self.to_relative_path(self.file_path, project_root)
        tags = [f"[file: {rel}]"]

        if upto in ("class", "func", "all") and self.class_name:
            tags.append(f"[class: {self.class_name}]")

        if upto in ("func", "all") and self.func_name:
            tags.append(f"[func: {self.func_name}]")

        if upto == "all":
            if self.line is not None:
                tags.append(f"[line: {self.line}]")
            if self.col is not None:
                tags.append(f"[col: {self.col}]")
            if self.score is not None:
                tags.append(f"[score: {self.score:.4f}]")
            if self.preview:
                # Avoid newlines in a single-line tag string
                prev = " ".join(self.preview.splitlines()).strip()
                if prev:
                    tags.append(f"[preview: {prev}]")
        return tags

    def to_tagged_upto_file(self, project_root: str):
        '''Convert the search result to a tagged string, upto file path.'''
        return " ".join(self._tag_components(project_root, upto="file"))

    def to_tagged_upto_class(self, project_root: str):
        '''Convert the search result to a tagged string, upto class.'''
        return " ".join(self._tag_components(project_root, upto="class"))

    def to_tagged_upto_func(self, project_root: str):
        '''Convert the search result to a tagged string, upto function.'''
        return " ".join(self._tag_components(project_root, upto="func"))

    def to_tagged_str(self, project_root: str):
        '''Convert the search result to a tagged string.'''
        return " ".join(self._tag_components(project_root, upto="all"))

    @staticmethod
    def collapse_to_file_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        '''Collapse search results to file level.'''
        seen: set[str] = set()
        lines: List[str] = []
        for item in lst:
            rel = SearchResult.to_relative_path(item.file_path, project_root)
            if rel not in seen:
                seen.add(rel)
                lines.append(item.to_tagged_upto_file(project_root))
        lines.sort()
        return "\n".join(lines)

    @staticmethod
    def collapse_to_method_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        '''Collapse search results to method level.'''
        seen: set[Tuple[str, Optional[str], Optional[str]]] = set()
        lines: List[str] = []
        for item in lst:
            rel = SearchResult.to_relative_path(item.file_path, project_root)
            key = (rel, item.class_name, item.func_name)
            if key not in seen:
                seen.add(key)
                lines.append(item.to_tagged_upto_func(project_root))
        lines.sort()
        return "\n".join(lines)
