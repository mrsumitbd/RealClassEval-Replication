from dataclasses import dataclass
from typing import Optional, Iterable, Set
import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line_no: Optional[int] = None
    snippet: Optional[str] = None

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
        # Normalize and attempt to produce a clean relative path
        try:
            if project_root:
                rel = os.path.relpath(os.path.abspath(
                    file_path), os.path.abspath(project_root))
                return rel
        except Exception:
            pass
        return os.path.normpath(file_path)

    def to_tagged_upto_file(self, project_root: str):
        rel = self.to_relative_path(self.file_path, project_root)
        return f"{rel}"

    def to_tagged_upto_class(self, project_root: str):
        '''Convert the search result to a tagged string, upto class.'''
        base = self.to_tagged_upto_file(project_root)
        if self.class_name:
            return f"{base}:{self.class_name}"
        return base

    def to_tagged_upto_func(self, project_root: str):
        base = self.to_tagged_upto_class(project_root)
        if self.func_name:
            return f"{base}:{self.func_name}"
        return base

    def to_tagged_str(self, project_root: str):
        s = self.to_tagged_upto_func(project_root)
        if self.line_no is not None:
            s = f"{s}@{self.line_no}"
        return s

    @staticmethod
    def collapse_to_file_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        tags: Set[str] = set()
        for item in lst:
            tags.add(item.to_tagged_upto_file(project_root))
        return "\n".join(sorted(tags))

    @staticmethod
    def collapse_to_method_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        tags: Set[str] = set()
        for item in lst:
            # Prefer method-level if available, else class-level, else file-level
            if item.func_name:
                tags.add(item.to_tagged_upto_func(project_root))
            elif item.class_name:
                tags.add(item.to_tagged_upto_class(project_root))
            else:
                tags.add(item.to_tagged_upto_file(project_root))
        return "\n".join(sorted(tags))
