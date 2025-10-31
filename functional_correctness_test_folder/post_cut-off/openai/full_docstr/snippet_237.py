
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""

    title: str
    snippet: str
    file_path: str
    line_number: int = 0
    language: str = field(default="Unknown")
    summary: str = field(default="")

    def __post_init__(self) -> None:
        """Infer language from file extension if not explicitly provided."""
        if self.language == "Unknown":
            _, ext = os.path.splitext(self.file_path)
            if ext:
                self.language = self.detect_language_from_extension(
                    ext.lower())

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        parts = [
            f"Title: {self.title}",
            f"Location: {self.file_path}:{self.line_number}",
            f"Language: {self.language}",
            f"Snippet:\n{self.snippet}",
        ]
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        return "\n".join(parts)

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        data = {
            "title": self.title,
            "snippet": self.snippet,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "language": self.language,
            "summary": self.summary,
        }
        return json.dumps(data, separators=(",", ":"))

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
        return "\n\n".join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """Calculate relative path from source root."""
        return os.path.relpath(file_path, start=source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
        mapping = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".c": "C",
            ".cpp": "C++",
            ".cxx": "C++",
            ".cs": "C#",
            ".rb": "Ruby",
            ".go": "Go",
            ".rs": "Rust",
            ".php": "PHP",
            ".html": "HTML",
            ".htm": "HTML",
            ".css": "CSS",
            ".json": "JSON",
            ".xml": "XML",
            ".md": "Markdown",
            ".yaml": "YAML",
            ".yml": "YAML",
            ".sh": "Shell",
            ".bat": "Batch",
            ".ps1": "PowerShell",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".m": "Objective-C",
            ".scala": "Scala",
            ".r": "R",
            ".pl": "Perl",
            ".sql": "SQL",
        }
        return mapping.get(extension.lower(), "Unknown")
