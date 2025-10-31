
from dataclasses import dataclass
import json
import os


@dataclass
class MultiSearchResult:
    file_path: str
    line_number: int
    line_content: str
    match_start: int
    match_end: int
    language: str = ""

    def __str__(self) -> str:
        lang = self.language if self.language else self.detect_language_from_extension(
            os.path.splitext(self.file_path)[1])
        return (f"{self.file_path}:{self.line_number}:"
                f"{self.match_start}-{self.match_end} [{lang}] "
                f"{self.line_content}")

    def to_json(self) -> str:
        return json.dumps({
            "file_path": self.file_path,
            "line_number": self.line_number,
            "line_content": self.line_content,
            "match_start": self.match_start,
            "match_end": self.match_end,
            "language": self.language
        })

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        return "\n".join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        return "\n".join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        return os.path.relpath(file_path, start=source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        ext = extension.lower().lstrip('.')
        mapping = {
            "py": "Python",
            "js": "JavaScript",
            "ts": "TypeScript",
            "java": "Java",
            "cpp": "C++",
            "c": "C",
            "cs": "C#",
            "rb": "Ruby",
            "go": "Go",
            "php": "PHP",
            "html": "HTML",
            "css": "CSS",
            "json": "JSON",
            "xml": "XML",
            "sh": "Shell",
            "bat": "Batch",
            "rs": "Rust",
            "swift": "Swift",
            "kt": "Kotlin",
            "m": "Objective-C",
            "scala": "Scala",
            "pl": "Perl",
            "r": "R",
            "lua": "Lua",
            "sql": "SQL",
            "md": "Markdown",
            "yml": "YAML",
            "yaml": "YAML",
            "dart": "Dart",
            "erl": "Erlang",
            "ex": "Elixir",
            "hs": "Haskell",
            "jl": "Julia",
            "groovy": "Groovy",
            "ps1": "PowerShell",
        }
        return mapping.get(ext, "Unknown")
