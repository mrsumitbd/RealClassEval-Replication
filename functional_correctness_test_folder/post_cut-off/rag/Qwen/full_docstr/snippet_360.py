
from dataclasses import dataclass, field
from typing import List, Optional
import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line_number: Optional[int] = None
    line_content: Optional[str] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.'''
        return os.path.relpath(file_path, project_root)

    def to_tagged_upto_file(self, project_root: str) -> str:
        '''Convert the search result to a tagged string, upto file path.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f"File: {relative_path}"

    def to_tagged_upto_class(self, project_root: str) -> str:
        '''Convert the search result to a tagged string, upto class.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.class_name:
            return f"File: {relative_path}, Class: {self.class_name}"
        return self.to_tagged_upto_file(project_root)

    def to_tagged_upto_func(self, project_root: str) -> str:
        '''Convert the search result to a tagged string, upto function.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        if self.func_name:
            return f"File: {relative_path}, Class: {self.class_name}, Function: {self.func_name}"
        return self.to_tagged_upto_class(project_root)

    def to_tagged_str(self, project_root: str) -> str:
        '''Convert the search result to a tagged string.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        tagged_str = f"File: {relative_path}"
        if self.class_name:
            tagged_str += f", Class: {self.class_name}"
        if self.func_name:
            tagged_str += f", Function: {self.func_name}"
        if self.line_number:
            tagged_str += f", Line: {self.line_number}"
        if self.line_content:
            tagged_str += f", Content: {self.line_content}"
        return tagged_str

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        '''Collapse search results to file level.'''
        file_set = set()
        for result in lst:
            relative_path = SearchResult.to_relative_path(
                result.file_path, project_root)
            file_set.add(relative_path)
        return "\n".join(sorted(file_set))

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        '''Collapse search results to method level.'''
        method_set = set()
        for result in lst:
            relative_path = SearchResult.to_relative_path(
                result.file_path, project_root)
            if result.func_name:
                method_set.add(
                    f"File: {relative_path}, Function: {result.func_name}")
            elif result.class_name:
                method_set.add(
                    f"File: {relative_path}, Class: {result.class_name}")
        return "\n".join(sorted(method_set))
