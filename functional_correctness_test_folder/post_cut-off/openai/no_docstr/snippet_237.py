
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class MultiSearchResult:
    file_path: str
    line: int
    snippet: str
    language: str = field(default="Unknown")

    def __post_init__(self) -> None:
        if self.language == "Unknown":
            _, ext = os.path.splitext(self.file_path)
            self.language = self.detect_language_from_extension(ext)

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line} [{self.language}] {self.snippet}"

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def to_jsonlines(cls, results: List["MultiSearchResult"]) -> str:
        return "\n".join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List["MultiSearchResult"]) -> str:
        return "\n".join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        abs_file = os.path.abspath(file_path)
        abs_source = os.path.abspath(source_path)
        return os.path.relpath(abs_file, start=abs_source)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        ext = extension.lower().lstrip(".")
        mapping = {
            "py": "Python",
            "js": "JavaScript",
            "ts": "TypeScript",
            "java": "Java",
            "c": "C",
            "cpp": "C++",
            "cxx": "C++",
            "cs": "C#",
            "rb": "Ruby",
            "go": "Go",
            "html": "HTML",
            "htm": "HTML",
            "css": "CSS",
            "json": "JSON",
            "xml": "XML",
            "md": "Markdown",
            "sh": "Shell",
            "bash": "Shell",
            "bat": "Batch",
            "ps1": "PowerShell",
            "sql": "SQL",
            "php": "PHP",
            "swift": "Swift",
            "kt": "Kotlin",
            "kts": "Kotlin",
            "rs": "Rust",
            "scala": "Scala",
            "pl": "Perl",
            "r": "R",
            "dart": "Dart",
            "lua": "Lua",
            "hs": "Haskell",
            "erl": "Erlang",
            "ex": "Elixir",
            "exs": "Elixir",
            "m": "Objective-C",
        }
        return mapping.get(ext, "Unknown")
