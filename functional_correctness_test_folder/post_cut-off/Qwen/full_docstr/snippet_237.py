
from dataclasses import dataclass, asdict
import json
import os


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''

    snippet: str
    file_path: str
    line_number: int
    score: float
    summary: str = None

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return (f"Snippet: {self.snippet}\n"
                f"File Path: {self.file_path}\n"
                f"Line Number: {self.line_number}\n"
                f"Score: {self.score}\n"
                f"Summary: {self.summary}")

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        return json.dumps(asdict(self), separators=(',', ':'))

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
        Returns:
            JSON Lines string (one JSON object per line)
        '''
        return '\n'.join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
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
            '.cpp': 'C++',
            '.h': 'C++',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.xml': 'XML',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.c': 'C',
            '.go': 'Go',
            '.ts': 'TypeScript',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.rust': 'Rust',
            '.perl': 'Perl',
            '.bash': 'Bash',
            '.sh': 'Shell',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.sql': 'SQL',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.dockerfile': 'Dockerfile',
            '.gitignore': 'Gitignore',
            '.env': 'Env',
            '.ini': 'INI',
            '.toml': 'TOML',
            '.lock': 'Lockfile',
            '.log': 'Logfile',
            '.csv': 'CSV',
            '.xlsx': 'Excel',
            '.pptx': 'PowerPoint',
            '.docx': 'Word',
            '.pdf': 'PDF',
            '.jpg': 'Image',
            '.jpeg': 'Image',
            '.png': 'Image',
            '.gif': 'Image',
            '.bmp': 'Image',
            '.tiff': 'Image',
            '.svg': 'SVG',
            '.mp4': 'Video',
            '.avi': 'Video',
            '.mov': 'Video',
            '.mkv': 'Video',
            '.mp3': 'Audio',
            '.wav': 'Audio',
            '.flac': 'Audio',
            '.aac': 'Audio',
            '.ogg': 'Audio',
            '.webm': 'Audio',
        }
        return language_map.get(extension.lower(), 'Unknown')
