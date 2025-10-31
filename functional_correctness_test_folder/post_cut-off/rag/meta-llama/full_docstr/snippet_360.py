
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    line_number: int
    entity_type: str
    entity_name: str
    text: str

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root.

        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.

        Returns:
            The relative path.
        """
        return str(Path(file_path).relative_to(Path(project_root)))

    def to_tagged_upto_file(self, project_root: str):
        """Convert the search result to a tagged string, upto file path."""
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'{relative_path}:{self.line_number}: {self.text}'

    def to_tagged_upto_class(self, project_root: str):
        """Convert the search result to a tagged string, upto class."""
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'{relative_path}:{self.line_number}: {self.entity_type} {self.entity_name}: {self.text}'

    def to_tagged_upto_func(self, project_root: str):
        """Convert the search result to a tagged string, upto function."""
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'{relative_path}:{self.line_number}: {self.entity_type} {self.entity_name}: {self.text}'

    def to_tagged_str(self, project_root: str):
        """Convert the search result to a tagged string."""
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'{relative_path}:{self.line_number}: {self.entity_type} {self.entity_name}: {self.text}'

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        """Collapse search results to file level."""
        files = set()
        for result in lst:
            relative_path = result.to_relative_path(
                result.file_path, project_root)
            files.add(relative_path)
        return '\n'.join(sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        """Collapse search results to method level."""
        methods = set()
        for result in lst:
            relative_path = result.to_relative_path(
                result.file_path, project_root)
            method = f'{relative_path}:{result.entity_name}'
            methods.add(method)
        return '\n'.join(sorted(methods))
