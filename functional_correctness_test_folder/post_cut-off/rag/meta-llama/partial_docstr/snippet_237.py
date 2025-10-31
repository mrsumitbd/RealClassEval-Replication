
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""
    file_path: str
    source_path: str
    snippet: str
    language: str
    start_line: int
    end_line: int

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        relative_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        return f"{relative_path}:{self.start_line}-{self.end_line}\n{self.snippet}"

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        data = {
            "file_path": self.file_path,
            "snippet": self.snippet,
            "language": self.language,
            "start_line": self.start_line,
            "end_line": self.end_line,
        }
        return json.dumps(data)

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        """Convert multiple MultiSearchResult objects to JSON Lines format.

        Args:
            results: List of MultiSearchResult objects

        Returns:
            JSON Lines string (one JSON object per line)
        """
        return '\n'.join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        """Convert multiple MultiSearchResult objects to a string."""
        return '\n\n'.join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """Calculate relative path from source root."""
        return str(Path(file_path).relative_to(Path(source_path)))

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
        language_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.js': 'JavaScript',
        }
        return language_map.get(extension.lower(), 'Unknown')
