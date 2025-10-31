
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
    match: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.'''
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
        if self.match:
            parts.append(f"<match>{self.match}</match>")
        return "::".join(parts)

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        files = set()
        for res in lst:
            rel_path = SearchResult.to_relative_path(
                res.file_path, project_root)
            files.add(rel_path)
        return "\n".join(f"<file>{f}</file>" for f in sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        methods = set()
        for res in lst:
            rel_path = SearchResult.to_relative_path(
                res.file_path, project_root)
            if res.class_name and res.func_name:
                key = (rel_path, res.class_name, res.func_name)
                methods.add(key)
            elif res.func_name:
                key = (rel_path, None, res.func_name)
                methods.add(key)

        def method_tag(key):
            rel_path, class_name, func_name = key
            tags = [f"<file>{rel_path}</file>"]
            if class_name:
                tags.append(f"<class>{class_name}</class>")
            tags.append(f"<func>{func_name}</func>")
            return "::".join(tags)
        return "\n".join(method_tag(k) for k in sorted(methods))
