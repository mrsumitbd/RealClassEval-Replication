
from dataclasses import dataclass
import os


@dataclass
class SearchResult:
    file_path: str
    line_number: int
    code_line: str
    class_name: str = None
    func_name: str = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"{relative_path}:{self.line_number}: {self.code_line.strip()}"

    def to_tagged_upto_class(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        class_tag = f"::{self.class_name}" if self.class_name else ""
        return f"{relative_path}{class_tag}:{self.line_number}: {self.code_line.strip()}"

    def to_tagged_upto_func(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        class_tag = f"::{self.class_name}" if self.class_name else ""
        func_tag = f"::{self.func_name}" if self.func_name else ""
        return f"{relative_path}{class_tag}{func_tag}:{self.line_number}: {self.code_line.strip()}"

    def to_tagged_str(self, project_root: str):
        return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        files = set(SearchResult.to_relative_path(
            item.file_path, project_root) for item in lst)
        return "\n".join(sorted(files))

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        methods = set()
        for item in lst:
            relative_path = SearchResult.to_relative_path(
                item.file_path, project_root)
            class_tag = f"::{item.class_name}" if item.class_name else ""
            func_tag = f"::{item.func_name}" if item.func_name else ""
            methods.add(f"{relative_path}{class_tag}{func_tag}")
        return "\n".join(sorted(methods))
