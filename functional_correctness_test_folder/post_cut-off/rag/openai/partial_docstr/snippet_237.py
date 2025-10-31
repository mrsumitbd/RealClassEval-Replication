
from __future__ import annotations

import json
import os
import pathlib
from dataclasses import dataclass, field
from typing import List, Optional, Sequence


@dataclass
class MultiSearchResult:
    """
    Enhanced search result with comprehensive snippet metadata.
    """

    # Core fields
    file_path: str
    snippet: str
    start_line: int = 0
    end_line: int = 0
    language: Optional[str] = None
    summary: Optional[str] = None

    # Derived fields (computed lazily)
    _relative_path: Optional[str] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.language is None:
            _, ext = os.path.splitext(self.file_path)
            self.language = self.detect_language_from_extension(
                ext.lstrip('.'))

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        rel_path = self.relative_path
        header = f"File: {rel_path} ({self.language}) Lines {self.start_line}-{self.end_line}"
        snippet = self.snippet.strip()
        return f"{header}\n\n{snippet}\n"

    @property
    def relative_path(self) -> str:
        """Cached relative path from the source root."""
        if self._relative_path is None:
            # Assume the source root is the current working directory
            self._relative_path = self.calculate_relative_path(
                self.file_path, os.getcwd()
            )
        return self._relative_path

    # ------------------------------------------------------------------
    # JSON / string conversions
    # ------------------------------------------------------------------
    def to_json(self) -> str:
        """Return LLM‑optimized JSON representation following the compact schema."""
        data = {
            "file": self.file_path,
            "relative_path": self.relative_path,
            "language": self.language,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "snippet": self.snippet,
        }
        if self.summary:
            data["summary"] = self.summary
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: Sequence["MultiSearchResult"]) -> str:
        """
        Convert multiple MultiSearchResult objects to JSON Lines format.

        Args:
            results: List of MultiSearchResult objects

        Returns:
            JSON Lines string (one JSON object per line)
        """
        return "\n".join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: Sequence["MultiSearchResult"]) -> str:
        """
        Convert multiple MultiSearchResult objects to a string.

        Args:
            results: List of MultiSearchResult objects

        Returns:
            A single string containing all results formatted with __str__.
        """
        return "\n".join(str(result) for result in results)

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """
        Calculate relative path from source root.

        Args:
            file_path: Absolute or relative path to the file.
            source_path: Root directory to calculate relative path from.

        Returns:
            Relative path string.
        """
        try:
            return os.path.relpath(file_path, source_path)
        except Exception:
            # Fallback: return the original path if relpath fails
            return file_path

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """
        Detect programming language from file extension.

        Args:
            extension: File extension without leading dot.

        Returns:
            Detected language name or 'unknown'.
        """
        mapping = {
            "py": "Python",
            "js": "JavaScript",
            "ts": "TypeScript",
            "java": "Java",
            "c": "C",
            "cpp": "C++",
            "cs": "C#",
            "rb": "Ruby",
            "go": "Go",
            "rs": "Rust",
            "php": "PHP",
            "swift": "Swift",
            "kt": "Kotlin",
            "m": "Objective‑C",
            "sh": "Shell",
            "bat": "Batch",
            "pl": "Perl",
            "hs": "Haskell",
            "scala": "Scala",
            "sql": "SQL",
            "html": "HTML",
            "css": "CSS",
            "json": "JSON",
            "xml": "XML",
            "yaml": "YAML",
            "yml": "YAML",
            "md": "Markdown",
            "txt": "Text",
        }
        return mapping.get(extension.lower(), "unknown")
