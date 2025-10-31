
from dataclasses import dataclass
import os


@dataclass
class SearchResult:
    file_path: str
    class_name: str = None
    func_name: str = None
    line_number: int = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"{relative_path}"

    def to_tagged_upto_class(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"{relative_path}::{self.class_name}" if self.class_name else f"{relative_path}"

    def to_tagged_upto_func(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.func_name:
            return f"{relative_path}::{self.class_name}::{self.func_name}" if self.class_name else f"{relative_path}::{self.func_name}"
        else:
            return self.to_tagged_upto_class(project_root)

    def to_tagged_str(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.line_number:
            return f"{relative_path}::{self.class_name}::{self.func_name}::{self.line_number}" if self.class_name and self.func_name else f"{relative_path}::{self.func_name}::{self.line_number}" if self.func_name else f"{relative_path}::{self.line_number}"
        else:
            return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        unique_files = set()
        for item in lst:
            unique_files.add(item.to_tagged_upto_file(project_root))
        return "\n".join(sorted(unique_files))

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        unique_methods = set()
        for item in lst:
            unique_methods.add(item.to_tagged_upto_func(project_root))
        return "\n".join(sorted(unique_methods))
