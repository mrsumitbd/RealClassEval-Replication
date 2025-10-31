
from dataclasses import dataclass, asdict
import json
import os
from typing import List


@dataclass
class MultiSearchResult:

    def __str__(self) -> str:
        return json.dumps(asdict(self), indent=2)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        return "\n".join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        return "\n".join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        return os.path.relpath(file_path, source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
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
