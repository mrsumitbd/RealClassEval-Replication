
from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json
import os


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    source_path: str
    line_start: int
    line_end: int
    snippet: str
    score: float
    summary: Optional[str] = None
    language: Optional[str] = None
    relative_path: Optional[str] = field(init=False, default=None)

    def __post_init__(self):
        self.relative_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        if not self.language:
            _, ext = os.path.splitext(self.file_path)
            self.language = self.detect_language_from_extension(ext)

    def __str__(self) -> str:
        lines = [
            f"File: {self.file_path}",
            f"Relative Path: {self.relative_path}",
            f"Lines: {self.line_start}-{self.line_end}",
            f"Score: {self.score:.4f}",
            f"Language: {self.language}",
        ]
        if self.summary:
            lines.append(f"Summary: {self.summary}")
        lines.append("Snippet:")
        lines.append(self.snippet)
        return "\n".join(lines)

    def to_json(self) -> str:
        d = asdict(self)
        return json.dumps(d, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        return "\n".join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        return "\n\n".join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        try:
            return os.path.relpath(file_path, source_path)
        except Exception:
            return file_path

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        ext = extension.lower().lstrip('.')
        mapping = {
            'py': 'Python',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'java': 'Java',
            'cpp': 'C++',
            'c': 'C',
            'cs': 'C#',
            'rb': 'Ruby',
            'go': 'Go',
            'php': 'PHP',
            'rs': 'Rust',
            'swift': 'Swift',
            'kt': 'Kotlin',
            'm': 'Objective-C',
            'scala': 'Scala',
            'sh': 'Shell',
            'bat': 'Batch',
            'pl': 'Perl',
            'r': 'R',
            'jl': 'Julia',
            'sql': 'SQL',
            'html': 'HTML',
            'css': 'CSS',
            'xml': 'XML',
            'json': 'JSON',
            'yaml': 'YAML',
            'yml': 'YAML',
            'md': 'Markdown',
            'tex': 'TeX',
        }
        return mapping.get(ext, 'Unknown')
