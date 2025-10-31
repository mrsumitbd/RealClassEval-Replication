
from dataclasses import dataclass
from typing import List


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    class_name: str = None
    method_name: str = None
    line_number: int = None
    line_content: str = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        """
        import os
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        """Convert the search result to a tagged string, upto file path."""
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"file:{rel_path}"

    def to_tagged_upto_class(self, project_root: str):
        """Convert the search result to a tagged string, upto class."""
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"file:{rel_path} class:{self.class_name}" if self.class_name else self.to_tagged_upto_file(project_root)

    def to_tagged_upto_func(self, project_root: str):
        """Convert the search result to a tagged string, upto function."""
        upto_class = self.to_tagged_upto_class(project_root)
        return f"{upto_class} method:{self.method_name}" if self.method_name else upto_class

    def to_tagged_str(self, project_root: str):
        """Convert the search result to a tagged string."""
        upto_func = self.to_tagged_upto_func(project_root)
        return f"{upto_func} line:{self.line_number} {self.line_content}" if self.line_number else upto_func

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        """Collapse search results to file level."""
        files = {result.to_tagged_upto_file(project_root) for result in lst}
        return "\n".join(sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        """Collapse search results to method level."""
        methods = {result.to_tagged_upto_func(project_root) for result in lst}
        return "\n".join(sorted(methods))
