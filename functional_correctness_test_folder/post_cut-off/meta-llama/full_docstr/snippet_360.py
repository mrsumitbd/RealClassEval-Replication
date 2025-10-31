
from dataclasses import dataclass
import os
from typing import List


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    line_number: int
    class_name: str
    func_name: str
    line_content: str

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.
        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.
        Returns:
            The relative path.
        '''
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        '''Convert the search result to a tagged string, upto file path.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"[{relative_path}:{self.line_number}] {self.line_content.strip()}"

    def to_tagged_upto_class(self, project_root: str):
        '''Convert the search result to a tagged string, upto class.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            return f"[{relative_path}:{self.class_name}:{self.line_number}] {self.line_content.strip()}"
        else:
            return self.to_tagged_upto_file(project_root)

    def to_tagged_upto_func(self, project_root: str):
        '''Convert the search result to a tagged string, upto function.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.func_name:
            return f"[{relative_path}:{self.class_name + '.' if self.class_name else ''}{self.func_name}:{self.line_number}] {self.line_content.strip()}"
        else:
            return self.to_tagged_upto_class(project_root)

    def to_tagged_str(self, project_root: str):
        '''Convert the search result to a tagged string.'''
        return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        '''Collapse search results to file level.'''
        file_paths = set(result.to_relative_path(
            result.file_path, project_root) for result in lst)
        return '\n'.join(f"- {file_path}" for file_path in file_paths)

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        '''Collapse search results to method level.'''
        method_signatures = set(
            f"{result.to_relative_path(result.file_path, project_root)}:{result.class_name + '.' if result.class_name else ''}{result.func_name}" for result in lst if result.func_name)
        return '\n'.join(f"- {method_signature}" for method_signature in method_signatures)
