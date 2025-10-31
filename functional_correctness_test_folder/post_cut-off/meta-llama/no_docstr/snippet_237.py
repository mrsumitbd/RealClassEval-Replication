
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class MultiSearchResult:
    file_path: str
    source_path: str
    line_number: int
    content: str
    language: str = None

    def __str__(self) -> str:
        relative_path = self.calculate_relative_path(
            self.file_path, self.source_path)
        return f"{relative_path}:{self.line_number}: {self.content.strip()}"

    def to_json(self) -> str:
        data = asdict(self)
        if not self.language:
            data['language'] = self.detect_language_from_extension(
                Path(self.file_path).suffix)
        return json.dumps(data)

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        return '\n'.join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        return '\n'.join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        return str(Path(file_path).relative_to(source_path))

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        language_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.js': 'JavaScript',
        }
        return language_map.get(extension.lower(), 'Unknown')
