
from dataclasses import dataclass
import os
from typing import List


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    line_number: int
    code_context: str
    name: str
    kind: str
    container: str

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
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"[{relative_path}:{self.line_number}] {self.code_context.strip()}"

    def to_tagged_upto_class(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.container:
            return f"[{relative_path}:{self.line_number}::{self.container}] {self.code_context.strip()}"
        else:
            return self.to_tagged_upto_file(project_root)

    def to_tagged_upto_func(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.kind == 'function' or self.kind == 'method':
            return f"[{relative_path}:{self.line_number}::{self.container}.{self.name}] {self.code_context.strip()}"
        else:
            return self.to_tagged_upto_class(project_root)

    def to_tagged_str(self, project_root: str):
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"[{relative_path}:{self.line_number}] {self.code_context.strip()}"

    @staticmethod
    def collapse_to_file_level(results: List['SearchResult'], project_root: str) -> str:
        file_paths = set(result.file_path for result in results)
        relative_paths = [SearchResult.to_relative_path(
            file_path, project_root) for file_path in file_paths]
        return '\n'.join(relative_paths)

    @staticmethod
    def collapse_to_method_level(results: List['SearchResult'], project_root: str) -> str:
        method_signatures = set(
            f"{SearchResult.to_relative_path(result.file_path, project_root)}:{result.container}.{result.name}" for result in results if result.kind in ['function', 'method'])
        return '\n'.join(method_signatures)
