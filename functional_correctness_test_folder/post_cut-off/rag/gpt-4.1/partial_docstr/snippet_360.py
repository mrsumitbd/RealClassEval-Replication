from dataclasses import dataclass
from typing import Optional, List

import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line_number: Optional[int] = None
    col_number: Optional[int] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        '''
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"<file>{rel_path}</file>"

    def to_tagged_upto_class(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            return f"<file>{rel_path}</file>::<class>{self.class_name}</class>"
        else:
            return f"<file>{rel_path}</file>"

    def to_tagged_upto_func(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        parts = [f"<file>{rel_path}</file>"]
        if self.class_name:
            parts.append(f"<class>{self.class_name}</class>")
        if self.func_name:
            parts.append(f"<func>{self.func_name}</func>")
        return "::".join(parts)

    def to_tagged_str(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        parts = [f"<file>{rel_path}</file>"]
        if self.class_name:
            parts.append(f"<class>{self.class_name}</class>")
        if self.func_name:
            parts.append(f"<func>{self.func_name}</func>")
        if self.line_number is not None:
            parts.append(f"<line>{self.line_number}</line>")
        if self.col_number is not None:
            parts.append(f"<col>{self.col_number}</col>")
        return "::".join(parts)

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        files = set()
        for r in lst:
            rel_path = SearchResult.to_relative_path(r.file_path, project_root)
            files.add(rel_path)
        return "\n".join(f"<file>{f}</file>" for f in sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        methods = set()
        for r in lst:
            rel_path = SearchResult.to_relative_path(r.file_path, project_root)
            if r.class_name and r.func_name:
                key = (rel_path, r.class_name, r.func_name)
                methods.add(key)
            elif r.func_name:
                key = (rel_path, None, r.func_name)
                methods.add(key)

        def format_method(tup):
            rel_path, class_name, func_name = tup
            parts = [f"<file>{rel_path}</file>"]
            if class_name:
                parts.append(f"<class>{class_name}</class>")
            if func_name:
                parts.append(f"<func>{func_name}</func>")
            return "::".join(parts)
        return "\n".join(format_method(t) for t in sorted(methods))
