
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Any
import json
import os


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    source_path: str
    snippet: str
    line_start: int
    line_end: int
    score: float
    repo: Optional[str] = None
    repo_url: Optional[str] = None
    file_url: Optional[str] = None
    language: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    extra: dict = field(default_factory=dict)

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        rel_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        lang = self.language or self.detect_language_from_extension(
            os.path.splitext(self.file_path)[1])
        header = f"[{self.repo or ''}] {rel_path}:{self.line_start}-{self.line_end} ({lang})"
        score_str = f"Score: {self.score:.4f}"
        title_str = f"Title: {self.title}" if self.title else ""
        summary_str = f"Summary: {self.summary}" if self.summary else ""
        url_str = f"URL: {self.file_url}" if self.file_url else ""
        lines = [
            header,
            score_str,
            title_str,
            summary_str,
            url_str,
            "Snippet:",
            self.snippet.strip(),
        ]
        # Remove empty lines
        return "\n".join([line for line in lines if line])

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        rel_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        lang = self.language or self.detect_language_from_extension(
            os.path.splitext(self.file_path)[1])
        data = {
            "repo": self.repo,
            "repo_url": self.repo_url,
            "file": rel_path,
            "file_url": self.file_url,
            "language": lang,
            "lines": [self.line_start, self.line_end],
            "score": self.score,
            "title": self.title,
            "summary": self.summary,
            "snippet": self.snippet,
        }
        if self.extra:
            data["extra"] = self.extra
        # Remove None values for compactness
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields
        Returns:
            JSON Lines string (one JSON object per line)
        '''
        return "\n".join([r.to_json() for r in results])

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return "\n\n".join([str(r) for r in results])

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        try:
            return os.path.relpath(file_path, source_path)
        except Exception:
            return file_path

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        ext = extension.lower().lstrip('.')
        mapping = {
            "py": "Python",
            "js": "JavaScript",
            "ts": "TypeScript",
            "java": "Java",
            "cpp": "C++",
            "cxx": "C++",
            "cc": "C++",
            "c": "C",
            "h": "C/C++ Header",
            "hpp": "C++ Header",
            "cs": "C#",
            "go": "Go",
            "rb": "Ruby",
            "php": "PHP",
            "rs": "Rust",
            "swift": "Swift",
            "kt": "Kotlin",
            "scala": "Scala",
            "sh": "Shell",
            "bat": "Batch",
            "pl": "Perl",
            "r": "R",
            "jl": "Julia",
            "lua": "Lua",
            "dart": "Dart",
            "m": "Objective-C/MATLAB",
            "sql": "SQL",
            "html": "HTML",
            "css": "CSS",
            "xml": "XML",
            "json": "JSON",
            "yaml": "YAML",
            "yml": "YAML",
            "md": "Markdown",
            "tex": "TeX",
            "ipynb": "Jupyter Notebook",
        }
        return mapping.get(ext, ext.upper() if ext else "Unknown")
