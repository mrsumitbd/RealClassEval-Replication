
from dataclasses import dataclass
import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
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
        return f'file:{relative_path}'

    def to_tagged_upto_class(self, project_root: str):
        '''Convert the search result to a tagged string, upto class.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'file:{relative_path} class:{self.class_name}'

    def to_tagged_upto_func(self, project_root: str):
        '''Convert the search result to a tagged string, upto function.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'file:{relative_path} class:{self.class_name} func:{self.func_name}'

    def to_tagged_str(self, project_root: str):
        '''Convert the search result to a tagged string.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'file:{relative_path} class:{self.class_name} func:{self.func_name} line:{self.line_number}'

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        '''Collapse search results to file level.'''
        files = set()
        for result in lst:
            relative_path = result.to_relative_path(
                result.file_path, project_root)
            files.add(relative_path)
        return '\n'.join(sorted(files))

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        '''Collapse search results to method level.'''
        methods = set()
        for result in lst:
            relative_path = result.to_relative_path(
                result.file_path, project_root)
            methods.add(f'{relative_path}::{result.func_name}')
        return '\n'.join(sorted(methods))
