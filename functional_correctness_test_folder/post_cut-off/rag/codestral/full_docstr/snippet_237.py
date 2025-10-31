
from dataclasses import dataclass
import json
from pathlib import Path
from typing import List, Optional


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    line_number: int
    snippet: str
    context_before: Optional[str] = None
    context_after: Optional[str] = None
    relevance_score: Optional[float] = None
    language: Optional[str] = None
    relative_path: Optional[str] = None
    file_size: Optional[int] = None
    last_modified: Optional[str] = None

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        output = f"File: {self.file_path}\n"
        output += f"Line: {self.line_number}\n"
        output += f"Snippet: {self.snippet}\n"
        if self.context_before:
            output += f"Context Before: {self.context_before}\n"
        if self.context_after:
            output += f"Context After: {self.context_after}\n"
        if self.relevance_score is not None:
            output += f"Relevance Score: {self.relevance_score:.2f}\n"
        if self.language:
            output += f"Language: {self.language}\n"
        if self.relative_path:
            output += f"Relative Path: {self.relative_path}\n"
        if self.file_size is not None:
            output += f"File Size: {self.file_size} bytes\n"
        if self.last_modified:
            output += f"Last Modified: {self.last_modified}\n"
        return output

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        data = {
            'file_path': self.file_path,
            'line_number': self.line_number,
            'snippet': self.snippet,
        }
        if self.context_before:
            data['context_before'] = self.context_before
        if self.context_after:
            data['context_after'] = self.context_after
        if self.relevance_score is not None:
            data['relevance_score'] = self.relevance_score
        if self.language:
            data['language'] = self.language
        if self.relative_path:
            data['relative_path'] = self.relative_path
        if self.file_size is not None:
            data['file_size'] = self.file_size
        if self.last_modified:
            data['last_modified'] = self.last_modified
        return json.dumps(data, indent=2)

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.'''
        return '\n'.join([result.to_json() for result in results])

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return '\n\n'.join([str(result) for result in results])

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        return str(Path(file_path).relative_to(source_path))

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        extension_to_language = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.java': 'Java',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C/C++ Header',
            '.hpp': 'C++ Header',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.m': 'Objective-C',
            '.scala': 'Scala',
            '.ts': 'TypeScript',
            '.sh': 'Shell',
            '.bash': 'Bash',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.md': 'Markdown',
            '.txt': 'Text',
        }
        return extension_to_language.get(extension.lower(), 'Unknown')
