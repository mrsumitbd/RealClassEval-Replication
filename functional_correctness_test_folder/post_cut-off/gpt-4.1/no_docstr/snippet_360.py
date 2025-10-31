
from dataclasses import dataclass
import os
from typing import List


@dataclass
class SearchResult:
    file_path: str
    class_name: str = None
    func_name: str = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"[FILE] {rel_path}"

    def to_tagged_upto_class(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            return f"[CLASS] {rel_path}::{self.class_name}"
        else:
            return f"[CLASS] {rel_path}"

    def to_tagged_upto_func(self, project_root: str):
        rel_path = self.to_relative_path(self.file_path, project_root)
        if self.class_name and self.func_name:
            return f"[FUNC] {rel_path}::{self.class_name}.{self.func_name}"
        elif self.func_name:
            return f"[FUNC] {rel_path}::{self.func_name}"
        elif self.class_name:
            return f"[FUNC] {rel_path}::{self.class_name}"
        else:
            return f"[FUNC] {rel_path}"

    def to_tagged_str(self, project_root: str):
        return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        files = set()
        for item in lst:
            files.add(SearchResult.to_relative_path(
                item.file_path, project_root))
        return "\n".join(f"[FILE] {f}" for f in sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        methods = set()
        for item in lst:
            rel_path = SearchResult.to_relative_path(
                item.file_path, project_root)
            if item.class_name and item.func_name:
                methods.add(
                    f"[FUNC] {rel_path}::{item.class_name}.{item.func_name}")
            elif item.func_name:
                methods.add(f"[FUNC] {rel_path}::{item.func_name}")
            elif item.class_name:
                methods.add(f"[FUNC] {rel_path}::{item.class_name}")
            else:
                methods.add(f"[FUNC] {rel_path}")
        return "\n".join(sorted(methods))
