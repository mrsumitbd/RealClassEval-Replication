from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib
import json
import os
from pathlib import Path


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""
    # Core identity and location
    file_path: str
    source_path: Optional[str] = None
    relative_path: Optional[str] = None
    url: Optional[str] = None
    repo: Optional[str] = None

    # Snippet metadata
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None
    snippet: Optional[str] = None
    context_before: Optional[str] = None
    context_after: Optional[str] = None
    summary: Optional[str] = None

    # Semantics
    title: Optional[str] = None
    query: Optional[str] = None
    score: Optional[float] = None
    symbols: Optional[List[str]] = field(default_factory=list)
    tags: Optional[List[str]] = field(default_factory=list)

    # Language and file info
    extension: Optional[str] = None
    language: Optional[str] = None

    # Extra/opaque payload
    extra: Optional[Dict[str, Any]] = field(default_factory=dict)

    # Stable identifier
    id: Optional[str] = None

    def __post_init__(self) -> None:
        # Normalize and compute relative path
        if self.source_path and not self.relative_path:
            self.relative_path = self.calculate_relative_path(
                self.file_path, self.source_path)

        # Compute extension
        if not self.extension:
            try:
                self.extension = Path(
                    self.file_path).suffix.lower().lstrip(".") or None
            except Exception:
                self.extension = None

        # Detect language
        if not self.language:
            self.language = self.detect_language_from_extension(
                self.extension or "")

        # Compute stable id
        if not self.id:
            h = hashlib.sha1()
            h.update((self.file_path or "").encode("utf-8"))
            h.update(str(self.start_line or -1).encode("utf-8"))
            h.update(str(self.end_line or -1).encode("utf-8"))
            h.update((self.snippet or "").encode("utf-8"))
            self.id = h.hexdigest()[:12]

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        loc = self.relative_path or self.file_path or ""
        line_span = ""
        if self.start_line is not None or self.end_line is not None:
            s = "" if self.start_line is None else str(self.start_line)
            e = "" if self.end_line is None else str(self.end_line)
            line_span = f":{s}-{e}" if s or e else ""
        lang = self.language or (self.extension or "unknown")
        score_str = f" score={self.score:.4f}" if isinstance(
            self.score, (int, float)) else ""
        title_str = f"\nTitle: {self.title}" if self.title else ""
        url_str = f"\nURL: {self.url}" if self.url else ""
        repo_str = f"\nRepo: {self.repo}" if self.repo else ""
        sym_str = f"\nSymbols: {', '.join(self.symbols)}" if self.symbols else ""
        tags_str = f"\nTags: {', '.join(self.tags)}" if self.tags else ""
        summary_str = f"\nSummary: {self.summary}" if self.summary else ""

        snippet = (self.snippet or "").rstrip()
        # Keep output compact: limit to 20 lines and 1000 chars
        if snippet:
            lines = snippet.splitlines()
            if len(lines) > 20:
                lines = lines[:20] + ["[...truncated...]"]
            snippet = "\n".join(lines)
            if len(snippet) > 1000:
                snippet = snippet[:1000] + "…"
            snippet = f"\nSnippet:\n{snippet}"

        return f"{loc}{line_span} [{lang}]{score_str}{title_str}{url_str}{repo_str}{sym_str}{tags_str}{summary_str}{snippet}"

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        obj = {
            "id": self.id,
            # path (prefer relative)
            "p": self.relative_path or self.file_path,
            "fp": self.file_path,  # full path
            "sp": self.source_path,  # source root
            "u": self.url,  # url
            "rp": self.repo,  # repository
            "t": self.title,  # title
            "q": self.query,  # query
            "l": self.language,  # language
            "ext": self.extension,  # file extension
            "s": self.start_line,  # start line
            "e": self.end_line,  # end line
            "cs": self.char_start,  # char start
            "ce": self.char_end,  # char end
            "sc": self.score,  # score
            "sn": self.snippet,  # snippet
            "cb": self.context_before,  # context before
            "ca": self.context_after,  # context after
            "sm": self.summary,  # summary
            "sy": self.symbols or [],  # symbols
            "tg": self.tags or [],  # tags
            "x": self.extra or {},  # extra
        }
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

    @classmethod
    def to_jsonlines(cls, results: List["MultiSearchResult"]) -> str:
        """Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields
        Returns:
            JSON Lines string (one JSON object per line)
        """
        if not results:
            return ""
        return "\n".join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: List["MultiSearchResult"]) -> str:
        """Convert multiple MultiSearchResult objects to a string."""
        if not results:
            return ""
        return "\n\n".join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """Calculate relative path from source root."""
        try:
            fp = Path(file_path).resolve()
            sp = Path(source_path).resolve()
            return str(fp.relative_to(sp))
        except Exception:
            # Fallback to os.path.relpath with guard for different drives on Windows
            try:
                return os.path.relpath(file_path, source_path)
            except Exception:
                return str(Path(file_path))

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
        if not extension:
            return "Unknown"
        ext = extension.lower().lstrip(".")
        mapping = {
            "py": "Python",
            "ipynb": "Jupyter Notebook",
            "js": "JavaScript",
            "jsx": "JavaScript",
            "ts": "TypeScript",
            "tsx": "TypeScript",
            "java": "Java",
            "kt": "Kotlin",
            "kts": "Kotlin",
            "rb": "Ruby",
            "rs": "Rust",
            "go": "Go",
            "php": "PHP",
            "cs": "C#",
            "c": "C",
            "h": "C/C++ Header",
            "cpp": "C++",
            "cxx": "C++",
            "cc": "C++",
            "hpp": "C++ Header",
            "m": "Objective-C",
            "mm": "Objective-C++",
            "swift": "Swift",
            "scala": "Scala",
            "r": "R",
            "pl": "Perl",
            "pm": "Perl",
            "sh": "Shell",
            "bash": "Shell",
            "zsh": "Shell",
            "ps1": "PowerShell",
            "sql": "SQL",
            "html": "HTML",
            "htm": "HTML",
            "xml": "XML",
            "xsd": "XML",
            "xsl": "XSLT",
            "css": "CSS",
            "scss": "SCSS",
            "less": "Less",
            "json": "JSON",
            "yaml": "YAML",
            "yml": "YAML",
            "toml": "TOML",
            "ini": "INI",
            "cfg": "INI",
            "md": "Markdown",
            "rst": "reStructuredText",
            "txt": "Text",
            "proto": "Protocol Buffers",
            "graphql": "GraphQL",
            "gql": "GraphQL",
            "dockerfile": "Dockerfile",
            "gradle": "Gradle",
            "makefile": "Makefile",
            "mk": "Makefile",
            "cmake": "CMake",
            "vue": "Vue",
            "svelte": "Svelte",
        }
        # Special-case some known 'word' filenames presented as extensions
        if ext in mapping:
            return mapping[ext]
        return "Unknown"
