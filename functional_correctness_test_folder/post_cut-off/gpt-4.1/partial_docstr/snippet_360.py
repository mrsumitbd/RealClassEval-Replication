
from dataclasses import dataclass
import os
from typing import List


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: str = None
    func_name: str = None
    line_no: int = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.'''
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"[FILE] {rel_path}"

    def to_tagged_upto_class(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            return f"[FILE] {rel_path} [CLASS] {self.class_name}"
        else:
            return f"[FILE] {rel_path}"

    def to_tagged_upto_func(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        parts = [f"[FILE] {rel_path}"]
        if self.class_name:
            parts.append(f"[CLASS] {self.class_name}")
        if self.func_name:
            parts.append(f"[FUNC] {self.func_name}")
        return " ".join(parts)

    def to_tagged_str(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        parts = [f"[FILE] {rel_path}"]
        if self.class_name:
            parts.append(f"[CLASS] {self.class_name}")
        if self.func_name:
            parts.append(f"[FUNC] {self.func_name}")
        if self.line_no is not None:
            parts.append(f"[LINE] {self.line_no}")
        return " ".join(parts)

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        files = set()
        for item in lst:
            rel_path = SearchResult.to_relative_path(
                item.file_path, project_root)
            files.add(rel_path)
        return "\n".join(f"[FILE] {f}" for f in sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        seen = set()
        results = []
        for item in lst:
            rel_path = SearchResult.to_relative_path(
                item.file_path, project_root)
            key = (rel_path, item.class_name, item.func_name)
            if key not in seen:
                seen.add(key)
                parts = [f"[FILE] {rel_path}"]
                if item.class_name:
                    parts.append(f"[CLASS] {item.class_name}")
                if item.func_name:
                    parts.append(f"[FUNC] {item.func_name}")
                results.append(" ".join(parts))
        return "\n".join(sorted(results))
