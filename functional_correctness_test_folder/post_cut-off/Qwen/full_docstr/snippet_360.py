
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
        '''Convert an absolute path to a path relative to the project root.'''
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str):
        '''Convert the search result to a tagged string, upto file path.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"File: {relative_path}"

    def to_tagged_upto_class(self, project_root: str):
        '''Convert the search result to a tagged string, upto class.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            return f"File: {relative_path}, Class: {self.class_name}"
        return self.to_tagged_upto_file(project_root)

    def to_tagged_upto_func(self, project_root: str):
        '''Convert the search result to a tagged string, upto function.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.func_name:
            return f"File: {relative_path}, Class: {self.class_name}, Function: {self.func_name}"
        return self.to_tagged_upto_class(project_root)

    def to_tagged_str(self, project_root: str):
        '''Convert the search result to a tagged string.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return (f"File: {relative_path}, Class: {self.class_name}, "
                f"Function: {self.func_name}, Line: {self.line_number}, "
                f"Content: {self.line_content}")

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        '''Collapse search results to file level.'''
        files = set()
        for result in lst:
            relative_path = SearchResult.to_relative_path(
                result.file_path, project_root)
            files.add(f"File: {relative_path}")
        return "\n".join(sorted(files))

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        '''Collapse search results to method level.'''
        methods = set()
        for result in lst:
            relative_path = SearchResult.to_relative_path(
                result.file_path, project_root)
            if result.func_name:
                methods.add(
                    f"File: {relative_path}, Function: {result.func_name}")
            elif result.class_name:
                methods.add(
                    f"File: {relative_path}, Class: {result.class_name}")
        return "\n".join(sorted(methods))
