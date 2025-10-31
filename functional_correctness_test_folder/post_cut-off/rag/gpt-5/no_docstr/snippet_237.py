from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import os


@dataclass
class MultiSearchResult:
    """Enhanced search result with comprehensive snippet metadata."""
    file_path: str
    source_path: str = ''
    snippet: str = ''
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    score: Optional[float] = None
    query: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.language:
            ext = Path(self.file_path).suffix
            self.language = self.detect_language_from_extension(ext)
        # Normalize snippet newlines
        if self.snippet is None:
            self.snippet = ''
        self.snippet = self.snippet.replace('\r\n', '\n').replace('\r', '\n')

    @property
    def relative_path(self) -> str:
        return self.calculate_relative_path(self.file_path, self.source_path)

    @property
    def line_count(self) -> Optional[int]:
        if self.start_line is not None and self.end_line is not None:
            return max(0, self.end_line - self.start_line + 1)
        if self.snippet:
            # Fallback to snippet lines
            return self.snippet.count('\n') + (0 if self.snippet.endswith('\n') else 1)
        return None

    @property
    def extension(self) -> str:
        return Path(self.file_path).suffix.lstrip('.').lower()

    def __str__(self) -> str:
        """Return enhanced formatted string representation."""
        parts: List[str] = []
        path_display = self.relative_path or self.file_path
        parts.append(path_display)
        if self.language:
            parts.append(f'lang={self.language}')
        if self.start_line is not None and self.end_line is not None:
            lc = self.line_count
            if lc is not None:
                parts.append(f'lines={self.start_line}-{self.end_line}({lc})')
            else:
                parts.append(f'lines={self.start_line}-{self.end_line}')
        elif self.line_count is not None:
            parts.append(f'lines=~{self.line_count}')
        if self.score is not None:
            parts.append(f'score={self.score:.4f}')
        header = ' | '.join(parts)
        body = self.snippet if self.snippet.endswith('\n') else (
            self.snippet + '\n') if self.snippet else ''
        return f'{header}\n{body}'.rstrip('\n')

    def to_json(self) -> str:
        """Return LLM-optimized JSON representation following the compact schema."""
        # Compact schema with short keys:
        # p: path (relative if available), ap: absolute path
        # l: language, e: extension
        # sl: start line, el: end line, lc: line count
        # s: score, t: snippet text, q: query, m: metadata
        payload: Dict[str, Any] = {
            'p': self.relative_path or self.file_path,
            'ap': str(self.file_path),
            'l': self.language,
            'e': self.extension or None,
            'sl': self.start_line,
            'el': self.end_line,
            'lc': self.line_count,
            's': self.score,
            't': self.snippet,
            'q': self.query,
            'm': self.metadata if self.metadata else None,
        }

        def keep(k: str, v: Any) -> bool:
            if v is None:
                return False
            if k == 't':
                return True  # keep snippet even if empty
            if isinstance(v, (str, list, dict)) and len(v) == 0:
                return False
            return True

        compact = {k: v for k, v in payload.items() if keep(k, v)}
        return json.dumps(compact, ensure_ascii=False, separators=(',', ':'))

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        """Convert multiple MultiSearchResult objects to JSON Lines format.
        Args:
            results: List of MultiSearchResult objects
            include_summary: Whether to include summary fields
        Returns:
            JSON Lines string (one JSON object per line)
        """
        return '\n'.join(r.to_json() for r in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        """Convert multiple MultiSearchResult objects to a string."""
        return '\n\n'.join(str(r) for r in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        """Calculate relative path from source root."""
        if not source_path:
            return ''
        try:
            f = Path(file_path).resolve()
        except Exception:
            f = Path(file_path)
        try:
            s = Path(source_path).resolve()
        except Exception:
            s = Path(source_path)
        # Try pathlib relative_to first
        try:
            return str(f.relative_to(s))
        except Exception:
            pass
        # Fallback to os.path.relpath (handles different drives with ValueError)
        try:
            return os.path.relpath(str(f), str(s))
        except Exception:
            return str(f)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        """Detect programming language from file extension."""
        ext = (extension or '').strip().lower().lstrip('.')
        if not ext:
            return 'Text'
        mapping = {
            'py': 'Python',
            'ipynb': 'Jupyter Notebook',
            'js': 'JavaScript',
            'jsx': 'JavaScript',
            'ts': 'TypeScript',
            'tsx': 'TypeScript',
            'mjs': 'JavaScript',
            'cjs': 'JavaScript',
            'java': 'Java',
            'c': 'C',
            'h': 'C/C++ Header',
            'hpp': 'C++ Header',
            'hh': 'C++ Header',
            'hxx': 'C++ Header',
            'cc': 'C++',
            'cpp': 'C++',
            'cxx': 'C++',
            'cs': 'C#',
            'go': 'Go',
            'rb': 'Ruby',
            'php': 'PHP',
            'rs': 'Rust',
            'kt': 'Kotlin',
            'kts': 'Kotlin',
            'swift': 'Swift',
            'm': 'Objective-C',
            'mm': 'Objective-C++',
            'scala': 'Scala',
            'sql': 'SQL',
            'sh': 'Shell',
            'bash': 'Shell',
            'zsh': 'Shell',
            'ps1': 'PowerShell',
            'yaml': 'YAML',
            'yml': 'YAML',
            'json': 'JSON',
            'toml': 'TOML',
            'ini': 'INI',
            'cfg': 'INI',
            'conf': 'Config',
            'md': 'Markdown',
            'rst': 'reStructuredText',
            'html': 'HTML',
            'htm': 'HTML',
            'css': 'CSS',
            'scss': 'SCSS',
            'less': 'Less',
            'vue': 'Vue',
            'svelte': 'Svelte',
            'r': 'R',
            'jl': 'Julia',
            'pl': 'Perl',
            'pm': 'Perl',
            'lua': 'Lua',
            'dart': 'Dart',
            'vb': 'Visual Basic',
            'asm': 'Assembly',
            'hs': 'Haskell',
            'erl': 'Erlang',
            'ex': 'Elixir',
            'exs': 'Elixir',
            'hx': 'Haxe',
            'gradle': 'Groovy',
            'groovy': 'Groovy',
            'properties': 'Properties',
            'bat': 'Batchfile',
            'dockerfile': 'Dockerfile',
            'tf': 'HCL',
            'tfvars': 'HCL',
            'proto': 'Protocol Buffers',
            'graphql': 'GraphQL',
            'gql': 'GraphQL',
            'xml': 'XML',
            'xsd': 'XML',
            'tsxproj': 'XML',
            'sln': 'Solution',
            'cmake': 'CMake',
            'makefile': 'Makefile',
            'mk': 'Makefile',
        }
        # Normalize well-known special filenames passed as "extension"
        if ext in ('makefile', 'dockerfile'):
            return mapping[ext]
        return mapping.get(ext, ext.upper() if len(ext) <= 6 else 'Text')
