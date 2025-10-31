
import os
from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root."""
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str) -> str:
        """Convert the search result to a tagged string, up to file path."""
        rel = self.to_relative_path(self.file_path, project_root)
        return f'[{rel}]({rel})'

    def to_tagged_upto_class(self, project_root: str) -> str:
        """Convert the search result to a tagged string, up to class."""
        rel = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            target = f'{rel}#{self.class_name}'
        else:
            target = rel
        return f'[{target}]({target})'

    def to_tagged_upto_func(self, project_root: str) -> str:
        """Convert the search result to a tagged string, up to function."""
        rel = self.to_relative_path(self.file_path, project_root)
        if self.class_name and self.func_name:
            target = f'{rel}#{self.class_name}.{self.func_name}'
        elif self.func_name:
            target = f'{rel}#{self.func_name}'
        else:
            target = rel
        return f'[{target}]({target})'

    def to_tagged_str(self, project_root: str) -> str:
        """Convert the search result to a tagged string."""
        return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse search results to file level."""
        unique: Set[str] = set()
        for res in lst:
            unique.add(res.to_tagged_upto_file(project_root))
        return "\n".join(sorted(unique))

    @staticmethod
    def collapse_to_method_level(lst: List["SearchResult"], project_root: str) -> str:
        """Collapse search results to method level."""
        unique: Set[str] = set()
        for res in lst:
            unique.add(res.to_tagged_upto_func(project_root))
        return "\n".join(sorted(unique))
