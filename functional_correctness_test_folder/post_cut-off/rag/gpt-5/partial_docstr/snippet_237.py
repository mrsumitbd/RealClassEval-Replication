from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, List
import json
import os


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""
    file_path: str
    snippet: str
    start_line: int
    end_line: int
    source_path: Optional[str] = None
    score: Optional[float] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.start_line > self.end_line:
            self.start_line, self.end_line = self.end_line, self.start_line
        if not self.language:
            self.language = self.detect_language_from_extension(self.extension)

    @property
    def file_name(self) -> str:
        return Path(self.file_path).name

    @property
    def extension(self) -> str:
        return Path(self.file_path).suffix.lstrip(".").lower()

    @property
    def relative_path(self) -> str:
        if not self.source_path:
            return self.file_path
        return self.calculate_relative_path(self.file_path, self.source_path)

    def __str__(self) -> str:
        line_range = f"L{self.start_line}" if self.start_line == self.end_line else f"L{self.start_line}-L{self.end_line}"
        lang = f" [{self.language}]" if self.language else ""
        score = f" score={round(self.score, 3)}" if self.score is not None else ""
        header = f"{self.relative_path}:{line_range}{lang}{score}"
        return f"{header}\n{self.snippet}"

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        data: Dict[str, Any] = {
            # path (relative if possible)
            "p": self.relative_path,
            "n": self.file_name,                    # file name
            "e": self.extension,                    # extension
            "l": self.language,                     # language
            "r": [self.start_line, self.end_line],  # line range
            "s": self.snippet.strip("\n"),          # snippet
        }
        if self.score is not None:
            data["sc"] = round(self.score, 6)
        if self.metadata:
            data["m"] = self.metadata
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def to_jsonlines(cls, results: List["MultiSearchResult"]) -> str:
        """Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields
        Returns:
            JSON Lines string (one JSON object per line)
        """
        return "\n".join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: List["MultiSearchResult"]) -> str:
        """Convert multiple MultiSearchResult objects to a string."""
        return "\n\n".join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """Calculate relative path from source root."""
        try:
            fp = Path(file_path).resolve()
            sp = Path(source_path).resolve()
            try:
                return str(fp.relative_to(sp))
            except ValueError:
                # Not a subpath, fall back to generic relpath (may contain ..)
                return os.path.relpath(str(fp), str(sp))
        except Exception:
            return file_path

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
        ext = (extension or "").lower().lstrip(".")
        mapping = {
            "py": "Python",
            "ipynb": "Jupyter Notebook",
            "js": "JavaScript",
            "mjs": "JavaScript",
            "cjs": "JavaScript",
            "ts": "TypeScript",
            "tsx": "TypeScript",
            "jsx": "JavaScript",
            "java": "Java",
            "c": "C",
            "h": "C/C++",
            "cpp": "C++",
            "cc": "C++",
            "cxx": "C++",
            "hpp": "C++",
            "hxx": "C++",
            "cs": "C#",
            "go": "Go",
            "rb": "Ruby",
            "php": "PHP",
            "rs": "Rust",
            "swift": "Swift",
            "kt": "Kotlin",
            "kts": "Kotlin",
            "sh": "Shell",
            "bash": "Shell",
            "ps1": "PowerShell",
            "pl": "Perl",
            "r": "R",
            "scala": "Scala",
            "lua": "Lua",
            "sql": "SQL",
            "html": "HTML",
            "htm": "HTML",
            "css": "CSS",
            "scss": "SCSS",
            "sass": "Sass",
            "xml": "XML",
            "json": "JSON",
            "md": "Markdown",
            "rst": "reStructuredText",
            "txt": "Text",
            "yaml": "YAML",
            "yml": "YAML",
            "toml": "TOML",
            "ini": "INI",
            "cfg": "INI",
            "bat": "Batchfile",
            "gradle": "Gradle",
            "makefile": "Makefile",
            "mk": "Makefile",
            "dockerfile": "Dockerfile",
        }
        if ext in mapping:
            return mapping[ext]
        return "Unknown" if not ext else ext.upper()
