
from dataclasses import dataclass
import os


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    line_number: int
    line_content: str
    class_name: str = None
    function_name: str = None

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
        return f"{relative_path}:{self.line_number}"

    def to_tagged_upto_class(self, project_root: str):
        tagged_upto_file = self.to_tagged_upto_file(project_root)
        if self.class_name:
            return f"{tagged_upto_file}::{self.class_name}"
        return tagged_upto_file

    def to_tagged_upto_func(self, project_root: str):
        tagged_upto_class = self.to_tagged_upto_class(project_root)
        if self.function_name:
            return f"{tagged_upto_class}::{self.function_name}"
        return tagged_upto_class

    def to_tagged_str(self, project_root: str):
        tagged_upto_func = self.to_tagged_upto_func(project_root)
        return f"{tagged_upto_func}: {self.line_content}"

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        file_level_results = {}
        for result in lst:
            tagged_upto_file = result.to_tagged_upto_file(project_root)
            if tagged_upto_file not in file_level_results:
                file_level_results[tagged_upto_file] = set()
            file_level_results[tagged_upto_file].add(result.line_content)

        output = []
        for tagged_upto_file, line_contents in file_level_results.items():
            output.append(f"{tagged_upto_file}: {', '.join(line_contents)}")
        return "\n".join(output)

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        method_level_results = {}
        for result in lst:
            tagged_upto_func = result.to_tagged_upto_func(project_root)
            if tagged_upto_func not in method_level_results:
                method_level_results[tagged_upto_func] = set()
            method_level_results[tagged_upto_func].add(result.line_content)

        output = []
        for tagged_upto_func, line_contents in method_level_results.items():
            output.append(f"{tagged_upto_func}: {', '.join(line_contents)}")
        return "\n".join(output)
