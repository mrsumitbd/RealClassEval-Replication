from dataclasses import dataclass
from typing import Iterable, List, Optional
import os


@dataclass
class SearchResult:
    file_path: str
    class_name: Optional[str] = None
    func_name: Optional[str] = None
    line_no: Optional[int] = None

    @staticmethod
    def to_relative_path(file_path: str, project_root: str) -> str:
        if not file_path:
            return ""
        norm_file = os.path.abspath(file_path)
        if project_root:
            norm_root = os.path.abspath(project_root)
            try:
                common = os.path.commonpath([norm_file, norm_root])
            except ValueError:
                common = ""
            if common and common == norm_root:
                rel = os.path.relpath(norm_file, norm_root)
            else:
                rel = norm_file
        else:
            rel = norm_file
        return rel.replace(os.sep, "/")

    def _base_tag(self, project_root: str) -> str:
        base = self.to_relative_path(self.file_path, project_root)
        if self.line_no is not None:
            return f"{base}:{self.line_no}"
        return base

    def to_tagged_upto_file(self, project_root: str):
        return self._base_tag(project_root)

    def to_tagged_upto_class(self, project_root: str):
        base = self._base_tag(project_root)
        if self.class_name:
            return f"{base}::{self.class_name}"
        return base

    def to_tagged_upto_func(self, project_root: str):
        base = self._base_tag(project_root)
        parts: List[str] = [base]
        if self.class_name:
            parts.append(self.class_name)
        if self.func_name:
            parts.append(self.func_name)
        return "::".join(parts)

    def to_tagged_str(self, project_root: str):
        return self.to_tagged_upto_func(project_root)

    @staticmethod
    def collapse_to_file_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        seen = set()
        out: List[str] = []
        for item in lst:
            tag = item.to_tagged_upto_file(project_root)
            if tag not in seen:
                seen.add(tag)
                out.append(tag)
        return "\n".join(out)

    @staticmethod
    def collapse_to_method_level(lst: Iterable["SearchResult"], project_root: str) -> str:
        seen = set()
        out: List[str] = []
        for item in lst:
            tag = item.to_tagged_upto_func(project_root)
            if tag not in seen:
                seen.add(tag)
                out.append(tag)
        return "\n".join(out)
