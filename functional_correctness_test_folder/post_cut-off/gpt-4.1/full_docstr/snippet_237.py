
from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json
import os


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    line_start: int
    line_end: int
    snippet: str
    score: float
    title: Optional[str] = None
    summary: Optional[str] = None
    language: Optional[str] = None
    relative_path: Optional[str] = None

    def __str__(self) -> str:
        parts = [
            f"File: {self.file_path}",
            f"Lines: {self.line_start}-{self.line_end}",
            f"Score: {self.score:.4f}",
        ]
        if self.title:
            parts.append(f"Title: {self.title}")
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        if self.language:
            parts.append(f"Language: {self.language}")
        if self.relative_path:
            parts.append(f"Relative Path: {self.relative_path}")
        parts.append("Snippet:\n" + self.snippet)
        return "\n".join(parts)

    def to_json(self) -> str:
        # Compact schema, omit None fields
        d = {k: v for k, v in asdict(self).items() if v is not None}
        return json.dumps(d, ensure_ascii=False, separators=(',', ':'))

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        lines = [r.to_json() for r in results]
        return "\n".join(lines)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        return "\n\n".join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        return os.path.relpath(file_path, start=source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        ext = extension.lower().lstrip('.')
        mapping = {
            'py': 'Python',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'java': 'Java',
            'cpp': 'C++',
            'cxx': 'C++',
            'cc': 'C++',
            'c': 'C',
            'h': 'C/C++ Header',
            'hpp': 'C++ Header',
            'cs': 'C#',
            'rb': 'Ruby',
            'go': 'Go',
            'rs': 'Rust',
            'php': 'PHP',
            'swift': 'Swift',
            'kt': 'Kotlin',
            'm': 'Objective-C',
            'scala': 'Scala',
            'sh': 'Shell',
            'bat': 'Batch',
            'pl': 'Perl',
            'lua': 'Lua',
            'r': 'R',
            'sql': 'SQL',
            'html': 'HTML',
            'css': 'CSS',
            'xml': 'XML',
            'json': 'JSON',
            'yaml': 'YAML',
            'yml': 'YAML',
            'md': 'Markdown',
            'tex': 'TeX',
            'dart': 'Dart',
            'erl': 'Erlang',
            'ex': 'Elixir',
            'exs': 'Elixir',
            'jl': 'Julia',
            'vb': 'Visual Basic',
            'f': 'Fortran',
            'f90': 'Fortran',
            'f95': 'Fortran',
            'groovy': 'Groovy',
            'coffee': 'CoffeeScript',
            'clj': 'Clojure',
            'hs': 'Haskell',
            'ps1': 'PowerShell',
            'psm1': 'PowerShell',
            'psd1': 'PowerShell',
        }
        return mapping.get(ext, 'Unknown')
