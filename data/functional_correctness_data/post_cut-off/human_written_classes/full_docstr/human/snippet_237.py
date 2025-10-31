from datetime import datetime
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""
    id: int
    content: str
    original_scores: list[float]
    source_uri: str
    relative_path: str
    language: str
    authors: list[str]
    created_at: datetime
    summary: str

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        lines = ['---', f'id: {self.id}', f'source: {self.source_uri}', f'path: {self.relative_path}', f'lang: {self.language}', f'created: {self.created_at.isoformat()}', f"authors: {', '.join(self.authors)}", f'scores: {self.original_scores}', '---', f'{self.summary}\n', f'```{self.language}', f'{self.content}', '```\n']
        return '\n'.join(lines)

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        json_obj = {'id': self.id, 'source': self.source_uri, 'path': self.relative_path, 'lang': self.language.lower(), 'created': self.created_at.isoformat() if self.created_at else '', 'author': ', '.join(self.authors), 'score': self.original_scores, 'code': self.content, 'summary': self.summary}
        return json.dumps(json_obj, separators=(',', ':'))

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        """Convert multiple MultiSearchResult objects to JSON Lines format.

        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields

        Returns:
            JSON Lines string (one JSON object per line)

        """
        return '\n'.join((result.to_json() for result in results))

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        """Convert multiple MultiSearchResult objects to a string."""
        return '\n\n'.join((str(result) for result in results))

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """Calculate relative path from source root."""
        try:
            return str(Path(file_path).relative_to(Path(source_path)))
        except ValueError:
            return Path(file_path).name

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
        try:
            return LanguageMapping.get_language_for_extension(extension).title()
        except ValueError:
            return 'Unknown'