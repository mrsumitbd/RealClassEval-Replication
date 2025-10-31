
import dataclasses
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    source_path: str
    snippet: str
    language: str = None

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return f"File: {self.file_path}\nSnippet: {self.snippet}"

    def to_json(self) -> str:
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
        return str(Path(file_path).relative_to(source_path))

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        language_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.js': 'JavaScript'
        }
        return language_map.get(extension.lower(), 'Unknown')


# Example usage:
if __name__ == "__main__":
    result1 = MultiSearchResult(
        file_path="/path/to/file1.py",
        source_path="/path/to",
        snippet="print('Hello World')",
        language=MultiSearchResult.detect_language_from_extension('.py')
    )
    result2 = MultiSearchResult(
        file_path="/path/to/file2.java",
        source_path="/path/to",
        snippet="System.out.println('Hello World');",
        language=MultiSearchResult.detect_language_from_extension('.java')
    )

    print(result1)
    print(result1.to_json())
    print(MultiSearchResult.to_jsonlines([result1, result2]))
    print(MultiSearchResult.to_string([result1, result2]))
    print(MultiSearchResult.calculate_relative_path(
        "/path/to/file.py", "/path/to"))
    print(MultiSearchResult.detect_language_from_extension('.py'))
