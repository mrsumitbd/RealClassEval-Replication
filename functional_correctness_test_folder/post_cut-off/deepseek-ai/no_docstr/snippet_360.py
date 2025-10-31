
from dataclasses import dataclass
import os


@dataclass
class SearchResult:

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"file:{relative_path}"

    def to_tagged_upto_class(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"class:{relative_path}:{self.class_name}"

    def to_tagged_upto_func(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"func:{relative_path}:{self.class_name}:{self.func_name}"

    def to_tagged_str(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"str:{relative_path}:{self.class_name}:{self.func_name}:{self.line_number}:{self.text}"

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        files = set()
        for item in lst:
            relative_path = SearchResult.to_relative_path(
                item.file_path, project_root)
            files.add(relative_path)
        return "\n".join(sorted(files))

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        methods = set()
        for item in lst:
            relative_path = SearchResult.to_relative_path(
                item.file_path, project_root)
            methods.add(f"{relative_path}:{item.class_name}:{item.func_name}")
        return "\n".join(sorted(methods))
