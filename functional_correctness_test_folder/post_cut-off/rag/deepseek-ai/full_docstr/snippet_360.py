
from dataclasses import dataclass
from typing import List


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    class_name: str = None
    method_name: str = None
    line_number: int = None
    code: str = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        """
        if file_path.startswith(project_root):
            return file_path[len(project_root):].lstrip('/')
        return file_path

    def to_tagged_upto_file(self, project_root: str):
        """Convert the search result to a tagged string, upto file path."""
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"file:{rel_path}"

    def to_tagged_upto_class(self, project_root: str):
        """Convert the search result to a tagged string, upto class."""
        if not self.class_name:
            return self.to_tagged_upto_file(project_root)
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"file:{rel_path} class:{self.class_name}"

    def to_tagged_upto_func(self, project_root: str):
        """Convert the search result to a tagged string, upto function."""
        if not self.method_name:
            return self.to_tagged_upto_class(project_root)
        rel_path = self.to_relative_path(self.file_path, project_root)
        return f"file:{rel_path} class:{self.class_name} method:{self.method_name}"

    def to_tagged_str(self, project_root: str):
        """Convert the search result to a tagged string."""
        rel_path = self.to_relative_path(self.file_path, project_root)
        tags = []
        if rel_path:
            tags.append(f"file:{rel_path}")
        if self.class_name:
            tags.append(f"class:{self.class_name}")
        if self.method_name:
            tags.append(f"method:{self.method_name}")
        if self.line_number is not None:
            tags.append(f"line:{self.line_number}")
        return ' '.join(tags)

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        """Collapse search results to file level."""
        files = set()
        for result in lst:
            files.add(result.to_tagged_upto_file(project_root))
        return '\n'.join(sorted(files))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        """Collapse search results to method level."""
        methods = set()
        for result in lst:
            methods.add(result.to_tagged_upto_func(project_root))
        return '\n'.join(sorted(methods))
