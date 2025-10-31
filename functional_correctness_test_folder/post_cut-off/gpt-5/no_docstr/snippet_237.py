from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MultiSearchResult:
    file_path: str
    source_path: str | None = None
    line: int | None = None
    start: int | None = None
    end: int | None = None
    snippet: str | None = None
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.language is None:
            self.language = self.detect_language_from_extension(
                os.path.splitext(self.file_path)[1]
            )

    def __str__(self) -> str:
        rel = self.calculate_relative_path(
            self.file_path, self.source_path or "")
        loc_parts = []
        if self.line is not None:
            loc_parts.append(str(self.line))
        if self.start is not None or self.end is not None:
            a = "" if self.start is None else str(self.start)
            b = "" if self.end is None else str(self.end)
            loc_parts.append(f"{a}-{b}".strip("-"))
        loc = ":" + ":".join(loc_parts) if loc_parts else ""
        snippet = (self.snippet or "").strip()
        if snippet:
            return f"{rel}{loc} | {snippet}"
        return f"{rel}{loc}"

    def to_json(self) -> str:
        data: dict[str, Any] = {
            "file_path": self.file_path,
            "relative_path": self.calculate_relative_path(self.file_path, self.source_path or ""),
            "source_path": self.source_path,
            "line": self.line,
            "start": self.start,
            "end": self.end,
            "snippet": self.snippet,
            "language": self.language,
            "metadata": self.metadata if self.metadata else None,
        }
        # remove None values
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        return "\n".join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: list['MultiSearchResult']) -> str:
        return "\n".join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        if not source_path:
            return file_path.replace("\\", "/")
        try:
            rel = os.path.relpath(file_path, start=source_path)
        except Exception:
            return file_path.replace("\\", "/")
        return rel.replace("\\", "/")

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        ext = extension.strip().lower()
        if not ext:
            return "unknown"
        if ext.startswith("."):
            ext = ext[1:]

        special_files = {
            "dockerfile": "docker",
            "makefile": "make",
        }
        if extension and not extension.startswith("."):
            name_lower = extension.lower()
            if name_lower in special_files:
                return special_files[name_lower]

        mapping = {
            "py": "python",
            "ipynb": "python",
            "js": "javascript",
            "mjs": "javascript",
            "cjs": "javascript",
            "ts": "typescript",
            "tsx": "tsx",
            "jsx": "jsx",
            "java": "java",
            "c": "c",
            "h": "c",
            "hpp": "cpp",
            "hh": "cpp",
            "hxx": "cpp",
            "cc": "cpp",
            "cpp": "cpp",
            "c++": "cpp",
            "cs": "csharp",
            "go": "go",
            "rb": "ruby",
            "php": "php",
            "rs": "rust",
            "kt": "kotlin",
            "kts": "kotlin",
            "swift": "swift",
            "m": "objective-c",
            "mm": "objective-cpp",
            "scala": "scala",
            "sh": "shell",
            "bash": "shell",
            "zsh": "shell",
            "ps1": "powershell",
            "sql": "sql",
            "html": "html",
            "htm": "html",
            "css": "css",
            "scss": "scss",
            "less": "less",
            "json": "json",
            "yaml": "yaml",
            "yml": "yaml",
            "toml": "toml",
            "ini": "ini",
            "cfg": "ini",
            "md": "markdown",
            "markdown": "markdown",
            "rst": "restructuredtext",
            "txt": "text",
            "xml": "xml",
            "vue": "vue",
            "svelte": "svelte",
            "dart": "dart",
            "erl": "erlang",
            "ex": "elixir",
            "exs": "elixir",
            "groovy": "groovy",
            "lua": "lua",
            "pl": "perl",
            "pm": "perl",
            "r": "r",
            "jl": "julia",
            "hs": "haskell",
            "ml": "ocaml",
            "mli": "ocaml",
            "nim": "nim",
            "coffee": "coffeescript",
            "gradle": "groovy",
            "dockerfile": "docker",
            "makefile": "make",
        }
        return mapping.get(ext, "unknown")
