
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""

    file_path: str
    snippet: str
    language: str = ""
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    summary: str = ""

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        parts = [f"File: {self.file_path}"]
        if self.language:
            parts.append(f"Language: {self.language}")
        if self.start_line is not None and self.end_line is not None:
            parts.append(f"Lines: {self.start_line}-{self.end_line}")
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        parts.append("Snippet:")
        parts.append(self.snippet)
        return "\n".join(parts)

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        data = {
            "file_path": self.file_path,
            "snippet": self.snippet,
            "language": self.language,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "summary": self.summary,
        }
        # Remove keys with None values for compactness
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, separators=(",", ":"))

    @classmethod
    def to_jsonlines(cls, results: List["MultiSearchResult"]) -> str:
        """Convert multiple MultiSearchResult objects to JSON Lines format.

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
        abs_file = os.path.abspath(file_path)
        abs_source = os.path.abspath(source_path)
        try:
            rel_path = os.path.relpath(abs_file, abs_source)
        except ValueError:
            # On Windows, if drives differ, return absolute path
            rel_path = abs_file
        return rel_path

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
        ext = extension.lower().lstrip(".")
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
            "yaml": "YAML",
            "yml": "YAML",
            "md": "Markdown",
            "txt": "Plain Text",
        }
        return mapping.get(ext, "Unknown")
