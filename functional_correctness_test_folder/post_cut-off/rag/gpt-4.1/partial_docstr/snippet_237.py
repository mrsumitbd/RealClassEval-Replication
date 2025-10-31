
from dataclasses import dataclass, asdict, field
from typing import List, Optional
import json
import os


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    snippet: str
    file_path: str
    source_path: str
    line_start: int
    line_end: int
    score: float
    repo: Optional[str] = None
    url: Optional[str] = None
    language: Optional[str] = None
    summary: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        rel_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        lang = self.language or self.detect_language_from_extension(
            os.path.splitext(self.file_path)[1])
        header = f"[{rel_path}:{self.line_start}-{self.line_end}]"
        if self.repo:
            header += f" ({self.repo})"
        if self.title:
            header += f" - {self.title}"
        if self.tags:
            header += f" [tags: {', '.join(self.tags)}]"
        if self.score is not None:
            header += f" [score: {self.score:.3f}]"
        if self.url:
            header += f"\nURL: {self.url}"
        if lang:
            header += f"\nLanguage: {lang}"
        if self.summary:
            header += f"\nSummary: {self.summary}"
        snippet_block = f"\n---\n{self.snippet}\n---"
        return f"{header}{snippet_block}"

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        rel_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        lang = self.language or self.detect_language_from_extension(
            os.path.splitext(self.file_path)[1])
        data = {
            "snippet": self.snippet,
            "file": rel_path,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "score": self.score,
            "repo": self.repo,
            "url": self.url,
            "language": lang,
            "summary": self.summary,
            "title": self.title,
            "tags": self.tags if self.tags else None,
        }
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
            "c": "C",
            "cs": "C#",
            "rb": "Ruby",
            "go": "Go",
            "rs": "Rust",
            "php": "PHP",
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
            "m": "Objective-C",
            "sql": "SQL",
            "html": "HTML",
            "css": "CSS",
            "xml": "XML",
            "json": "JSON",
            "yaml": "YAML",
            "yml": "YAML",
            "md": "Markdown",
            "ipynb": "Jupyter Notebook",
        }
        return mapping.get(ext, ext.upper() if ext else "Unknown")
