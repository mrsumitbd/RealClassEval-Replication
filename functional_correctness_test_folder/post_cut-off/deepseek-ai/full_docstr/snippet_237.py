
from dataclasses import dataclass
import json
import os
from typing import List


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return str(self.__dict__)

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        return json.dumps(self.__dict__)

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields
        Returns:
            JSON Lines string (one JSON object per line)
        '''
        return '\n'.join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return '\n'.join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        return os.path.relpath(file_path, source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.java': 'Java',
            '.c': 'C',
            '.cpp': 'C++',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.ts': 'TypeScript',
            '.sh': 'Shell',
            '.pl': 'Perl',
            '.lua': 'Lua',
            '.r': 'R',
            '.m': 'Objective-C',
            '.scala': 'Scala',
            '.hs': 'Haskell',
            '.ml': 'OCaml',
        }
        return language_map.get(extension.lower(), 'Unknown')
