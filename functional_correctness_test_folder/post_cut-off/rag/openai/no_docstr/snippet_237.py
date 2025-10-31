
import json
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""

    # Core attributes
    file_path: str
    snippet: str
    start_line: int = 0
    end_line: int = 0
    summary: Optional[str] = None
    # Optional language field; if not provided, it will be inferred from the file extension
    language: Optional[str] = None

    def __post_init__(self) -> None:
        # Infer language if not explicitly set
        if not self.language:
            _, ext = os.path.splitext(self.file_path)
            self.language = self.detect_language_from_extension(ext.lower())

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        rel_path = self.calculate_relative_path(self.file_path, os.getcwd())
        lines = f"File: {rel_path}"
        if self.start_line or self.end_line:
            lines += f" (lines {self.start_line}-{self.end_line})"
        lines += f"\nLanguage: {self.language}"
        lines += f"\n\nSnippet:\n{self.snippet}"
        if self.summary:
            lines += f"\n\nSummary:\n{self.summary}"
        return lines

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        data = {
            "file_path": self.file_path,
            "relative_path": self.calculate_relative_path(self.file_path, os.getcwd()),
            "snippet": self.snippet,
            "language": self.language,
            "start_line": self.start_line,
            "end_line": self.end_line,
        }
        if self.summary:
            data["summary"] = self.summary
        return json.dumps(data, separators=(",", ":"))

    @classmethod
    def to_jsonlines(cls, results: List["MultiSearchResult"]) -> str:
        """Convert multiple MultiSearchResult objects to JSON Lines format."""
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
            ".cs": "C#",
            ".rb": "Ruby",
            ".go": "Go",
            ".rs": "Rust",
            ".php": "PHP",
            ".html": "HTML",
            ".css": "CSS",
            ".json": "JSON",
            ".xml": "XML",
            ".yaml": "YAML",
            ".yml": "YAML",
            ".sh": "Shell",
            ".bat": "Batch",
            ".ps1": "PowerShell",
            ".sql": "SQL",
            ".md": "Markdown",
        }
        return mapping.get(extension.lower(), "Unknown")
