
from dataclasses import dataclass, asdict
import json
import os


@dataclass
class MultiSearchResult:
    query: str
    file_path: str
    line_number: int
    line_content: str

    def __str__(self) -> str:
        return f"Query: {self.query}, File: {self.file_path}, Line: {self.line_number}, Content: {self.line_content}"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=4)

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        return '\n'.join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        return '\n'.join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        return os.path.relpath(file_path, source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        language_map = {
            '.py': 'Python',
            '.java': 'Java',
            '.cpp': 'C++',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.txt': 'Text',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.xml': 'XML',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.c': 'C',
            '.h': 'C Header',
            '.go': 'Go',
            '.ts': 'TypeScript',
            '.swift': 'Swift',
            '.scala': 'Scala',
            '.rust': 'Rust',
            '.perl': 'Perl',
            '.bash': 'Bash',
            '.sh': 'Shell',
            '.sql': 'SQL',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.dockerfile': 'Dockerfile',
            '.gitignore': 'Gitignore',
            '.env': 'Environment Variables',
        }
        return language_map.get(extension.lower(), 'Unknown')
