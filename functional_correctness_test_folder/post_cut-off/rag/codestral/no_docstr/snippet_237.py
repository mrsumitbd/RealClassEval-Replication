
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    line_number: int
    snippet: str
    context: str
    relevance_score: float
    language: str = None
    relative_path: str = None
    summary: str = None

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return f"File: {self.file_path}\nLine: {self.line_number}\nScore: {self.relevance_score}\nSnippet:\n{self.snippet}\nContext:\n{self.context}"

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        data = {
            'file': self.file_path,
            'line': self.line_number,
            'snippet': self.snippet,
            'context': self.context,
            'score': self.relevance_score,
            'language': self.language,
            'relative_path': self.relative_path,
            'summary': self.summary
        }
        return json.dumps(data, indent=2)

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.'''
        return '\n'.join([result.to_json() for result in results])

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return '\n\n'.join([str(result) for result in results])

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        return str(Path(file_path).relative_to(source_path))

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        language_map = {
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
            '.pl': 'Perl',
            '.lua': 'Lua',
            '.r': 'R',
            '.dart': 'Dart',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.md': 'Markdown',
            '.txt': 'Text',
        }
        return language_map.get(extension.lower(), 'Unknown')
