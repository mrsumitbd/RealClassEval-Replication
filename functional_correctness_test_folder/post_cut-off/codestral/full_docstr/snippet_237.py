
from dataclasses import dataclass
import json
import os
from typing import List


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return f"MultiSearchResult({self.__dict__})"

    def to_json(self) -> str:
        '''Return LLM-optimized JSON representation following the compact schema.'''
        return json.dumps(self.__dict__)

    @classmethod
    def to_jsonlines(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.'''
        return '\n'.join(result.to_json() for result in results)

    @classmethod
    def to_string(cls, results: List['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to a string.'''
        return '\n'.join(str(result) for result in results)

    @staticmethod
    def calculate_relative_path(file_path: str, source_path: str) -> str:
        '''Calculate relative path from source root.'''
        return os.path.relpath(file_path, source_path)

    @staticmethod
    def detect_language_from_extension(extension: str) -> str:
        '''Detect programming language from file extension.'''
        extension_to_language = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.java': 'Java',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C/C++ Header',
            '.hpp': 'C++ Header',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.ts': 'TypeScript',
            '.scala': 'Scala',
            '.m': 'Objective-C',
            '.mm': 'Objective-C++',
            '.r': 'R',
            '.pl': 'Perl',
            '.sh': 'Shell',
            '.bash': 'Bash',
            '.zsh': 'Zsh',
            '.lua': 'Lua',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.toml': 'TOML',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.csv': 'CSV',
            '.sql': 'SQL',
            '.graphql': 'GraphQL',
            '.vue': 'Vue',
            '.svelte': 'Svelte',
            '.jsx': 'JSX',
            '.tsx': 'TSX',
            '.dart': 'Dart',
            '.clj': 'Clojure',
            '.cljs': 'ClojureScript',
            '.edn': 'edn',
            '.elm': 'Elm',
            '.erl': 'Erlang',
            '.ex': 'Elixir',
            '.exs': 'Elixir',
            '.fs': 'F#',
            '.fsi': 'F# Interface',
            '.fsx': 'F# Script',
            '.hs': 'Haskell',
            '.jl': 'Julia',
            '.nim': 'Nim',
            '.ml': 'OCaml',
            '.mli': 'OCaml Interface',
            '.purs': 'PureScript',
            '.rkt': 'Racket',
            '.scm': 'Scheme',
            '.scala': 'Scala',
            '.sc': 'SuperCollider',
            '.st': 'Smalltalk',
            '.v': 'Verilog',
            '.sv': 'SystemVerilog',
            '.vhd': 'VHDL',
            '.vhdl': 'VHDL',
            '.vb': 'Visual Basic',
            '.vbs': 'VBScript',
            '.ps1': 'PowerShell',
            '.psm1': 'PowerShell Module',
            '.psd1': 'PowerShell Data',
            '.ps1xml': 'PowerShell XML',
            '.tcl': 'Tcl',
            '.tk': 'Tk',
            '.tex': 'TeX',
            '.bib': 'BibTeX',
            '.sty': 'LaTeX Style',
            '.cls': 'LaTeX Class',
            '.dtx': 'LaTeX Documented Macro File',
            '.ins': 'LaTeX Installation File',
            '.asy': 'Asymptote',
            '.asy': 'Asymptote',
            '.d': 'D',
            '.pas': 'Pascal',
            '.pp': 'Pascal',
            '.lisp': 'Lisp',
            '.lsp': 'Lisp',
            '.pro': 'Prolog',
            '.pl': 'Prolog',
            '.prolog': 'Prolog',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
            '.sc': 'Scala',
            '.scala': 'Scala',
