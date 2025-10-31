
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""

    file_path: str
    line_number: int
    snippet: str
    summary: Optional[str] = None
    language: Optional[str] = None
    relative_path: Optional[str] = None

    def __post_init__(self) -> None:
        # Detect language from file extension if not provided
        if self.language is None:
            _, ext = os.path.splitext(self.file_path)
            self.language = self.detect_language_from_extension(
                ext.lstrip("."))
        # Compute relative path if not provided
        if self.relative_path is None:
            # Default source root is current working directory
            self.relative_path = self.calculate_relative_path(
                self.file_path, os.getcwd())

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        parts = [
            f"{self.relative_path}:{self.line_number}",
            f"[{self.language}]",
            self.snippet.strip(),
        ]
        if self.summary:
            parts.append(f"// {self.summary.strip()}")
        return " ".join(parts)

    def to_json(self) -> str:
        """Return JSON representation of the result."""
        data = {
            "file_path": self.file_path,
            "relative_path": self.relative_path,
            "line_number": self.line_number,
            "snippet": self.snippet,
            "summary": self.summary,
            "language": self.language,
        }
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: List["MultiSearchResult"]) -> str:
        """
        Convert multiple MultiSearchResult objects to JSON Lines format.

        Args:
            results: List of MultiSearchResult objects

        Returns:
            JSON Lines string (one JSON object per line)
        """
        return "\n".join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List["MultiSearchResult"]) -> str:
        """Convert multiple MultiSearchResult objects to a string."""
        return "\n".join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """Calculate relative path from source root."""
        return os.path.relpath(file_path, source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
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
            "m": "Objective-C",
            "scala": "Scala",
            "sh": "Shell",
            "bat": "Batch",
            "pl": "Perl",
            "hs": "Haskell",
            "sql": "SQL",
            "html": "HTML",
            "css": "CSS",
            "json": "JSON",
            "xml": "XML",
            "yml": "YAML",
            "yaml": "YAML",
        }
        return mapping.get(extension.lower(), "Unknown")
