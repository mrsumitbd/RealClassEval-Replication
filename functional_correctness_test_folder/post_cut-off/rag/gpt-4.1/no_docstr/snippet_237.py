
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Any
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
    repo: Optional[str] = None
    repo_url: Optional[str] = None
    file_url: Optional[str] = None
    language: Optional[str] = None
    summary: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)
    extra: Optional[dict] = field(default_factory=dict)

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        rel_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        lang = self.language or self.detect_language_from_extension(
            os.path.splitext(self.file_path)[1])
        lines = [
            f"Repository: {self.repo or '-'}",
            f"File: {rel_path} (lines {self.line_start}-{self.line_end})",
            f"Language: {lang}",
            f"Score: {self.score:.4f}",
        ]
        if self.title:
            lines.insert(0, f"Title: {self.title}")
        if self.tags:
            lines.append(f"Tags: {', '.join(self.tags)}")
        if self.summary:
            lines.append(f"Summary: {self.summary}")
        if self.file_url:
            lines.append(f"File URL: {self.file_url}")
        lines.append("Snippet:")
        lines.append(self.snippet)
        return "\n".join(lines)

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        rel_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        lang = self.language or self.detect_language_from_extension(
            os.path.splitext(self.file_path)[1])
        data = {
            "repo": self.repo,
            "file": rel_path,
            "lines": [self.line_start, self.line_end],
            "score": self.score,
            "snippet": self.snippet,
            "language": lang,
        }
        if self.title:
            data["title"] = self.title
        if self.tags:
            data["tags"] = self.tags
        if self.summary:
            data["summary"] = self.summary
        if self.repo_url:
            data["repo_url"] = self.repo_url
        if self.file_url:
            data["file_url"] = self.file_url
        if self.extra:
            data["extra"] = self.extra
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.'''
        return "\n".join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return "\n\n".join(str(r) for r in results)

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
            "bash": "Shell",
            "zsh": "Shell",
            "pl": "Perl",
            "r": "R",
            "jl": "Julia",
            "lua": "Lua",
            "sql": "SQL",
            "html": "HTML",
            "css": "CSS",
            "xml": "XML",
            "json": "JSON",
            "yaml": "YAML",
            "yml": "YAML",
            "md": "Markdown",
            "tex": "TeX",
            "dart": "Dart",
            "m": "Objective-C",
            "mm": "Objective-C++",
            "vb": "Visual Basic",
            "groovy": "Groovy",
            "erl": "Erlang",
            "ex": "Elixir",
            "exs": "Elixir",
            "hs": "Haskell",
            "ps1": "PowerShell",
            "bat": "Batch",
            "makefile": "Makefile",
            "dockerfile": "Dockerfile",
        }
        return mapping.get(ext, ext if ext else "Unknown")
