
import dataclasses
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return json.dumps(asdict(self), indent=2)

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        return json.dumps(asdict(self))

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
        Returns:
            JSON Lines string (one JSON object per line)
        '''
        return '\n'.join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return '\n\n'.join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        return str(Path(file_path).relative_to(Path(source_path)))

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        language_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.js': 'JavaScript',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.swift': 'Swift',
            '.php': 'PHP',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.rust': 'Rust',
        }
        return language_map.get(extension.lower(), 'Unknown')


# Example usage:
if __name__ == "__main__":
    @dataclass
    class ExampleMultiSearchResult(MultiSearchResult):
        file_path: str
        source_path: str
        extension: str
        content: str

    result1 = ExampleMultiSearchResult(
        file_path='/path/to/file1.py',
        source_path='/path/to',
        extension='.py',
        content='print("Hello World")'
    )
    result2 = ExampleMultiSearchResult(
        file_path='/path/to/file2.java',
        source_path='/path/to',
        extension='.java',
        content='System.out.println("Hello World");'
    )

    print(result1)
    print(result1.to_json())
    print(MultiSearchResult.to_jsonlines([result1, result2]))
    print(MultiSearchResult.to_string([result1, result2]))
    print(MultiSearchResult.calculate_relative_path(
        '/path/to/file.py', '/path/to'))
    print(MultiSearchResult.detect_language_from_extension('.py'))
