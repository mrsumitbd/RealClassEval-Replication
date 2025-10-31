
from dataclasses import dataclass, asdict
import json
import os


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    snippet: str
    line_number: int
    language: str
    summary: str

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return (f"File: {self.file_path}\n"
                f"Language: {self.language}\n"
                f"Line: {self.line_number}\n"
                f"Snippet: {self.snippet}\n"
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
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.html': 'HTML',
            '.css': 'CSS',
            '.ts': 'TypeScript',
            '.go': 'Go',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.rs': 'Rust',
            '.pl': 'Perl',
            '.sh': 'Shell',
            '.sql': 'SQL',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.c': 'C',
            '.h': 'C',
            '.m': 'Objective-C',
            '.mm': 'Objective-C++',
            '.dart': 'Dart',
            '.r': 'R',
            '.jl': 'Julia',
            '.hs': 'Haskell',
            '.lua': 'Lua',
            '.groovy': 'Groovy',
            '.tsv': 'TSV',
            '.csv': 'CSV',
            '.tex': 'LaTeX',
            '.texi': 'Texinfo',
            '.texinfo': 'Texinfo',
            '.rst': 'reStructuredText',
            '.adoc': 'AsciiDoc',
            '.asciidoc': 'AsciiDoc',
            '.mdown': 'Markdown',
            '.markdown': 'Markdown',
            '.mdwn': 'Markdown',
            '.mkd': 'Markdown',
            '.mdtxt': 'Markdown',
            '.mdtext': 'Markdown',
            '.mdx': 'Markdown',
            '.toml': 'TOML',
            '.ini': 'INI',
            '.cfg': 'INI',
            '.conf': 'INI',
            '.properties': 'Properties',
            '.env': 'Environment Variables',
            '.graphql': 'GraphQL',
            '.gql': 'GraphQL',
            '.graphqls': 'GraphQL',
            '.graphqlschema': 'GraphQL',
            '.gqls': 'GraphQL',
            '.gqlschema': 'GraphQL',
            '.svelte': 'Svelte',
            '.vue': 'Vue.js',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript React',
            '.jsx': 'JavaScript React',
            '.dart': 'Dart',
            '.dartlang': 'Dart',
            '.dart.js': 'Dart',
            '.dart.js.map': 'Dart',
            '.dart.map': 'Dart',
            '.dart.snapshot': 'Dart',
            '.dart.deps': 'Dart',
            '.dart.dill': 'Dart',
            '.dart.dill.deps': 'Dart',
            '.dart.dill.part': 'Dart',
            '.dart.dill.part.deps': 'Dart',
            '.dart.dill.part.snapshot': 'Dart',
            '.dart.dill.snapshot': 'Dart',
            '.dart.dill.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.deps': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot.part.snapshot': 'Dart',
            '.dart.dill.snapshot.part.snapshot.part
