from dataclasses import dataclass
from pathlib import Path

@dataclass
class SearchResult:
    """Dataclass to hold search results."""
    file_path: str
    start: int | None
    end: int | None
    class_name: str | None
    func_name: str | None
    code: str

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        """Convert an absolute path to a path relative to the project root.

        Args:
            - file_path (str): The absolute path.
            - project_root (str): Absolute path of the project root dir.

        Returns:
            The relative path.
        """
        if Path(file_path).is_absolute():
            return str(Path(file_path).relative_to(project_root))
        else:
            return file_path

    def to_tagged_upto_file(self, project_root: str):
        """Convert the search result to a tagged string, upto file path."""
        rel_path = self.to_relative_path(self.file_path, project_root)
        file_part = f'<file>{rel_path}</file>'
        return file_part

    def to_tagged_upto_class(self, project_root: str):
        """Convert the search result to a tagged string, upto class."""
        prefix = self.to_tagged_upto_file(project_root)
        class_part = f'<class>{self.class_name}</class>' if self.class_name is not None else ''
        return f'{prefix}\n{class_part}'

    def to_tagged_upto_func(self, project_root: str):
        """Convert the search result to a tagged string, upto function."""
        prefix = self.to_tagged_upto_class(project_root)
        func_part = f'<func>{self.func_name}</func>' if self.func_name is not None else ''
        return f'{prefix}{func_part}'

    def to_tagged_str(self, project_root: str):
        """Convert the search result to a tagged string."""
        prefix = self.to_tagged_upto_func(project_root)
        code_part = f'<code>\n{self.code}\n</code>'
        return f'{prefix}\n{code_part}'

    @staticmethod
    def collapse_to_file_level(lst, project_root: str) -> str:
        """Collapse search results to file level."""
        res = dict()
        for r in lst:
            if r.file_path not in res:
                res[r.file_path] = 1
            else:
                res[r.file_path] += 1
        res_str = ''
        for file_path, count in res.items():
            rel_path = SearchResult.to_relative_path(file_path, project_root)
            file_part = f'<file>{rel_path}</file>'
            res_str += f'- {file_part} ({count} matches)\n'
        return res_str

    @staticmethod
    def collapse_to_method_level(lst, project_root: str) -> str:
        """Collapse search results to method level."""
        res = dict()
        for r in lst:
            if r.file_path not in res:
                res[r.file_path] = dict()
            func_str = r.func_name if r.func_name is not None else 'Not in a function'
            if func_str not in res[r.file_path]:
                res[r.file_path][func_str] = 1
            else:
                res[r.file_path][func_str] += 1
        res_str = ''
        for file_path, funcs in res.items():
            rel_path = SearchResult.to_relative_path(file_path, project_root)
            file_part = f'<file>{rel_path}</file>'
            for func, count in funcs.items():
                if func == 'Not in a function':
                    func_part = func
                else:
                    func_part = f'<func>{func}</func>'
                res_str += f'- {file_part}{func_part} ({count} matches)\n'
        return res_str