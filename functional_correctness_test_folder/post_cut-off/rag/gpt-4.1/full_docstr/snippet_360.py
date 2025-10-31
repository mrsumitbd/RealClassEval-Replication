from dataclasses import dataclass
from typing import Optional, List, Any
import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line_number: Optional[int] = None
    col_number: Optional[int] = None
    match_text: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        '''
        file_path = os.path.abspath(file_path)
        project_root = os.path.abspath(project_root)
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"<file>{rel_path}</file>"

    def to_tagged_upto_class(self, project_root: str):
        s = self.to_tagged_upto_file(project_root)
        if self.class_name:
            s += f" <class>{self.class_name}</class>"
        return s

    def to_tagged_upto_func(self, project_root: str):
        s = self.to_tagged_upto_class(project_root)
        if self.func_name:
            s += f" <func>{self.func_name}</func>"
        return s

    def to_tagged_str(self, project_root: str):
        s = self.to_tagged_upto_func(project_root)
        if self.line_number is not None:
            s += f" <line>{self.line_number}</line>"
        if self.col_number is not None:
            s += f" <col>{self.col_number}</col>"
        if self.match_text is not None:
            s += f" <match>{self.match_text}</match>"
        return s

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        files = set()
        for r in lst:
            rel_path = SearchResult.to_relative_path(r.file_path, project_root)
            files.add(rel_path)
        return "\n".join(f"<file>{f}</file>" for f in sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        seen = set()
        out = []
        for r in lst:
            rel_path = SearchResult.to_relative_path(r.file_path, project_root)
            class_part = f"<class>{r.class_name}</class>" if r.class_name else ""
            func_part = f"<func>{r.func_name}</func>" if r.func_name else ""
            key = (rel_path, r.class_name, r.func_name)
            if key not in seen:
                seen.add(key)
                s = f"<file>{rel_path}</file>"
                if class_part:
                    s += f" {class_part}"
                if func_part:
                    s += f" {func_part}"
                out.append(s)
        return "\n".join(out)
