
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class SearchResult:
    '''Dataclass to hold search results.'''
    file_path: str
    class_name: str = ''
    func_name: str = ''
    line_number: int = 0
    line_content: str = ''

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        '''Convert an absolute path to a path relative to the project root.'''
        return str(Path(file_path).relative_to(project_root))

    def to_tagged_upto_file(self, project_root: str) -> str:
        '''Convert the search result to a tagged string, upto file.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'<file>{relative_path}</file>'

    def to_tagged_upto_class(self, project_root: str) -> str:
        '''Convert the search result to a tagged string, upto class.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'<file>{relative_path}</file><class>{self.class_name}</class>'

    def to_tagged_upto_func(self, project_root: str) -> str:
        '''Convert the search result to a tagged string, upto function.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return f'<file>{relative_path}</file><class>{self.class_name}</class><func>{self.func_name}</func>'

    def to_tagged_str(self, project_root: str) -> str:
        '''Convert the search result to a fully tagged string.'''
        relative_path = self.to_relative_path(self.file_path, project_root)
        return (f'<file>{relative_path}</file>'
                f'<class>{self.class_name}</class>'
                f'<func>{self.func_name}</func>'
                f'<line>{self.line_number}</line>'
                f'<content>{self.line_content}</content>')

    @staticmethod
    def collapse_to_file_level(lst: List['SearchResult'], project_root: str) -> str:
        '''Collapse a list of search results to a string, grouped by file.'''
        file_dict = {}
        for result in lst:
            relative_path = SearchResult.to_relative_path(
                result.file_path, project_root)
            if relative_path not in file_dict:
                file_dict[relative_path] = []
            file_dict[relative_path].append(result)

        output = []
        for file_path, results in file_dict.items():
            output.append(f'<file>{file_path}</file>')
            for result in results:
                output.append(
                    f'  <class>{result.class_name}</class><func>{result.func_name}</func><line>{result.line_number}</line><content>{result.line_content}</content>')
        return '\n'.join(output)

    @staticmethod
    def collapse_to_method_level(lst: List['SearchResult'], project_root: str) -> str:
        '''Collapse a list of search results to a string, grouped by method.'''
        method_dict = {}
        for result in lst:
            relative_path = SearchResult.to_relative_path(
                result.file_path, project_root)
            method_key = (relative_path, result.class_name, result.func_name)
            if method_key not in method_dict:
                method_dict[method_key] = []
            method_dict[method_key].append(result)

        output = []
        for (file_path, class_name, func_name), results in method_dict.items():
            output.append(
                f'<file>{file_path}</file><class>{class_name}</class><func>{func_name}</func>')
            for result in results:
                output.append(
                    f'  <line>{result.line_number}</line><content>{result.line_content}</content>')
        return '\n'.join(output)
