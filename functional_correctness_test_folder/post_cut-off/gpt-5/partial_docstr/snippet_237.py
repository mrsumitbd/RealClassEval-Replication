from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    path: str
    source_root: Optional[str] = None
    repository: Optional[str] = None
    extension: Optional[str] = None
    language: Optional[str] = None
    symbol: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    snippet: Optional[str] = None
    context_before: Optional[str] = None
    context_after: Optional[str] = None
    score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    relative_path: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.extension:
            _, ext = os.path.splitext(self.path)
            self.extension = ext or None
        if not self.language and self.extension:
            self.language = self.detect_language_from_extension(self.extension)
        if not self.relative_path:
            self.relative_path = self.calculate_relative_path(
                self.path, self.source_root or "")
        # Normalize lines
        if self.line_start is not None and self.line_end is not None:
            if self.line_end < self.line_start:
                self.line_start, self.line_end = self.line_end, self.line_start

    def __str__(self) -> str:
        loc = ""
        if self.line_start is not None and self.line_end is not None:
            if self.line_start == self.line_end:
                loc = f":{self.line_start}"
            else:
                loc = f":{self.line_start}-{self.line_end}"
        elif self.line_start is not None:
            loc = f":{self.line_start}"

        path_display = self.relative_path or self.path
        header_bits = [
            path_display + loc,
            f"lang={self.language}" if self.language else None,
            f"score={self.score:.4f}" if isinstance(
                self.score, (int, float)) else None,
            f"symbol={self.symbol}" if self.symbol else None,
            f"repo={self.repository}" if self.repository else None,
        ]
        header = " | ".join(bit for bit in header_bits if bit)

        parts = [header]
        if self.context_before:
            parts.append(self.context_before.rstrip("\n"))
        if self.snippet:
            parts.append(self.snippet.rstrip("\n"))
        if self.context_after:
            parts.append(self.context_after.rstrip("\n"))
        return "\n".join(parts)

    def to_json(self) -> str:
        payload = {
            "path": self.path,
            "relative_path": self.relative_path,
            "source_root": self.source_root,
            "repository": self.repository,
            "extension": self.extension,
            "language": self.language,
            "symbol": self.symbol,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "snippet": self.snippet,
            "context_before": self.context_before,
            "context_after": self.context_after,
            "score": self.score,
            "metadata": self.metadata or {},
        }
        return json.dumps(payload, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields
        Returns:
            JSON Lines string (one JSON object per line)
        '''
        return "\n".join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return "\n\n".join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        try:
            if source_path:
                return os.path.relpath(os.path.abspath(file_path), os.path.abspath(source_path))
            return os.path.normpath(file_path)
        except Exception:
            return file_path

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        ext = extension.lower().lstrip(".")
        mapping = {
            "py": "Python",
            "pyw": "Python",
            "ipynb": "Jupyter Notebook",
            "js": "JavaScript",
            "mjs": "JavaScript",
            "cjs": "JavaScript",
            "ts": "TypeScript",
            "tsx": "TypeScript",
            "jsx": "JavaScript",
            "json": "JSON",
            "yml": "YAML",
            "yaml": "YAML",
            "toml": "TOML",
            "ini": "INI",
            "cfg": "INI",
            "xml": "XML",
            "html": "HTML",
            "htm": "HTML",
            "css": "CSS",
            "scss": "SCSS",
            "sass": "Sass",
            "less": "Less",
            "md": "Markdown",
            "rst": "reStructuredText",
            "txt": "Text",
            "sh": "Shell",
            "bash": "Shell",
            "zsh": "Shell",
            "ps1": "PowerShell",
            "bat": "Batch",
            "cmd": "Batch",
            "c": "C",
            "h": "C",
            "cpp": "C++",
            "cxx": "C++",
            "hpp": "C++",
            "hh": "C++",
            "cc": "C++",
            "cs": "C#",
            "java": "Java",
            "kt": "Kotlin",
            "kts": "Kotlin",
            "go": "Go",
            "rs": "Rust",
            "rb": "Ruby",
            "php": "PHP",
            "pl": "Perl",
            "pm": "Perl",
            "r": "R",
            "jl": "Julia",
            "sql": "SQL",
            "swift": "Swift",
            "m": "Objective-C",
            "mm": "Objective-C++",
            "mat": "MATLAB",
            "mli": "OCaml",
            "ml": "OCaml",
            "hs": "Haskell",
            "lua": "Lua",
            "dart": "Dart",
            "scala": "Scala",
            "groovy": "Groovy",
            "asm": "Assembly",
            "s": "Assembly",
            "vb": "Visual Basic",
            "fish": "Shell",
            "dockerfile": "Dockerfile",
            "docker": "Dockerfile",
            "makefile": "Makefile",
            "mk": "Makefile",
            "gradle": "Gradle",
            "properties": "Properties",
        }
        if ext in ("dockerfile", "makefile"):
            return mapping[ext]
        return mapping.get(ext, "Text")
