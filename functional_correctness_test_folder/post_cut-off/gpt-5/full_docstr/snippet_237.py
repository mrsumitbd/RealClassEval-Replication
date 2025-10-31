from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''

    # Core identifiers
    file_path: str
    snippet: str

    # Optional metadata
    title: Optional[str] = None
    source_root: Optional[str] = None
    repo: Optional[str] = None
    url: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    score: Optional[float] = None
    language: Optional[str] = None
    metadata: Optional[Dict[str, object]] = None

    # Derived
    relative_path: str = field(init=False)

    def __post_init__(self) -> None:
        self.relative_path = self.calculate_relative_path(
            self.file_path, self.source_root or "")
        if self.language is None:
            _, ext = os.path.splitext(self.file_path)
            self.language = self.detect_language_from_extension(ext)
        if self.line_start is not None and self.line_end is None:
            self.line_end = self.line_start
        if self.metadata is None:
            self.metadata = {}

    def __str__(self) -> str:
        parts = []
        path_part = self.relative_path or self.file_path
        loc = ""
        if self.line_start is not None and self.line_end is not None:
            loc = f":{self.line_start}-{self.line_end}"
        parts.append(f"{path_part}{loc}")
        meta_bits = []
        if self.language:
            meta_bits.append(self.language)
        if self.score is not None:
            meta_bits.append(f"score={self.score:.4f}")
        if meta_bits:
            parts.append(f" ({', '.join(meta_bits)})")
        if self.title:
            parts.append(f" - {self.title}")
        header = "".join(parts)
        body = self.snippet if self.snippet is not None else ""
        return f"{header}\n{body}".rstrip()

    def to_json(self) -> str:
        obj = {
            # path (relative if available)
            "p": self.relative_path or self.file_path,
            "fp": self.file_path,                       # full path
            "u": self.url,                              # canonical URL if available
            "r": self.repo,                             # repository name or id
            "l": self.language,                         # language
            "s": self.score,                            # relevance score
            "ls": self.line_start,                      # line start
            "le": self.line_end,                        # line end
            "t": self.title,                            # title
            "sn": self.snippet,                         # snippet text
            "m": self.metadata if self.metadata else None,  # additional metadata
        }
        compact = {k: v for k, v in obj.items() if v is not None}
        return json.dumps(compact, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields
        Returns:
            JSON Lines string (one JSON object per line)
        '''
        return "\n".join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return "\n\n".join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        if not file_path:
            return ""
        if not source_path:
            return os.path.normpath(file_path)
        try:
            return os.path.relpath(os.path.normpath(file_path), os.path.normpath(source_path))
        except Exception:
            return os.path.normpath(file_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        if not extension:
            return "Text"
        ext = extension.lower().lstrip(".")
        mapping = {
            "py": "Python",
            "ipynb": "Jupyter Notebook",
            "js": "JavaScript",
            "jsx": "JavaScript",
            "ts": "TypeScript",
            "tsx": "TypeScript",
            "mjs": "JavaScript",
            "cjs": "JavaScript",
            "java": "Java",
            "c": "C",
            "h": "C/C++ Header",
            "cc": "C++",
            "cpp": "C++",
            "cxx": "C++",
            "hpp": "C++ Header",
            "cs": "C#",
            "go": "Go",
            "rb": "Ruby",
            "php": "PHP",
            "rs": "Rust",
            "kt": "Kotlin",
            "kts": "Kotlin",
            "m": "Objective-C",
            "mm": "Objective-C++",
            "swift": "Swift",
            "scala": "Scala",
            "sql": "SQL",
            "sh": "Shell",
            "bash": "Shell",
            "zsh": "Shell",
            "ps1": "PowerShell",
            "r": "R",
            "jl": "Julia",
            "pl": "Perl",
            "pm": "Perl",
            "lua": "Lua",
            "yaml": "YAML",
            "yml": "YAML",
            "toml": "TOML",
            "json": "JSON",
            "ndjson": "JSON Lines",
            "md": "Markdown",
            "markdown": "Markdown",
            "rst": "reStructuredText",
            "ini": "INI",
            "cfg": "Config",
            "conf": "Config",
            "txt": "Text",
            "html": "HTML",
            "htm": "HTML",
            "css": "CSS",
            "scss": "SCSS",
            "less": "Less",
            "xml": "XML",
            "proto": "Protocol Buffers",
            "dart": "Dart",
            "groovy": "Groovy",
            "gradle": "Gradle",
            "makefile": "Make",
            "mk": "Make",
            "dockerfile": "Dockerfile",
            "tf": "Terraform",
            "tfvars": "Terraform",
            "tsx.snap": "Snapshot",
            "snap": "Snapshot",
        }
        return mapping.get(ext, "Text")
