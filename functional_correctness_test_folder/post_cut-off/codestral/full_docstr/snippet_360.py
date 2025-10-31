
from dataclasses import dataclass
import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: str = None
    func_name: str = None
    line_number: int = None
    line_content: str = None

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
        return f"file:{relative_path}"

    def to_tagged_upto_class(self, project_root: str):
        '''Convert the search result to a tagged string, upto class.'''
        tagged_upto_file = self.to_tagged_upto_file(project_root)
        if self.class_name:
            return f"{tagged_upto_file},class:{self.class_name}"
        return tagged_upto_file

    def to_tagged_upto_func(self, project_root: str):
        '''Convert the search result to a tagged string, upto function.'''
        tagged_upto_class = self.to_tagged_upto_class(project_root)
        if self.func_name:
            return f"{tagged_upto_class},func:{self.func_name}"
        return tagged_upto_class

    def to_tagged_str(self, project_root: str):
        '''Convert the search result to a tagged string.'''
        tagged_upto_func = self.to_tagged_upto_func(project_root)
        if self.line_number:
            return f"{tagged_upto_func},line:{self.line_number}"
        return tagged_upto_func

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        '''Collapse search results to file level.'''
        unique_files = set()
        for result in lst:
            unique_files.add(result.to_tagged_upto_file(project_root))
        return "\n".join(sorted(unique_files))

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        '''Collapse search results to method level.'''
        unique_methods = set()
        for result in lst:
            unique_methods.add(result.to_tagged_upto_func(project_root))
        return "\n".join(sorted(unique_methods))
