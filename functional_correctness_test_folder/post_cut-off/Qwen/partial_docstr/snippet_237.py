
from dataclasses import dataclass, asdict
import json
import os


@dataclass
class MultiSearchResult:
    '''Enhanced search result with comprehensive snippet metadata.'''
    file_path: str
    snippet: str
    line_number: int
    summary: str = None

    def __str__(self) -> str:
        '''Return enhanced formatted string representation.'''
        return (f"File: {self.file_path}\n"
                f"Line: {self.line_number}\n"
                f"Snippet: {self.snippet}\n"
                f"Summary: {self.summary}\n")

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=4)

    @classmethod
    def to_jsonlines(cls, results: list['MultiSearchResult']) -> str:
        '''Convert multiple MultiSearchResult objects to JSON Lines format.'''
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
            '.java': 'Java',
            '.cpp': 'C++',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.go': 'Go',
            '.ts': 'TypeScript',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.rust': 'Rust',
            '.r': 'R',
            '.pl': 'Perl',
            '.sh': 'Shell',
            '.sql': 'SQL',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.txt': 'Text',
            '.c': 'C',
            '.h': 'C',
            '.hpp': 'C++',
            '.cs': 'C#',
            '.vb': 'VB.NET',
            '.php': 'PHP',
            '.jsp': 'JSP',
            '.asp': 'ASP',
            '.aspx': 'ASP.NET',
            '.jsp': 'JSP',
            '.tsx': 'TypeScript React',
            '.jsx': 'JavaScript React',
            '.vue': 'Vue.js',
            '.svelte': 'Svelte',
            '.tsv': 'TSV',
            '.csv': 'CSV',
            '.log': 'Log',
            '.ini': 'INI',
            '.toml': 'TOML',
            '.dockerfile': 'Dockerfile',
            '.gitignore': 'Gitignore',
            '.dockerignore': 'Dockerignore',
            '.env': 'Environment Variables',
            '.lock': 'Lock File',
            '.config': 'Configuration File',
            '.bak': 'Backup File',
            '.tmp': 'Temporary File',
            '.log': 'Log File',
            '.mdx': 'MDX',
            '.graphql': 'GraphQL',
            '.gql': 'GraphQL',
            '.graphqls': 'GraphQL Schema',
            '.prisma': 'Prisma',
            '.sol': 'Solidity',
            '.proto': 'Protocol Buffers',
            '.proto3': 'Protocol Buffers',
            '.proto2': 'Protocol Buffers',
            '.graphql': 'GraphQL',
            '.gql': 'GraphQL',
            '.graphqls': 'GraphQL Schema',
            '.prisma': 'Prisma',
            '.sol': 'Solidity',
            '.proto': 'Protocol Buffers',
            '.proto3': 'Protocol Buffers',
            '.proto2': 'Protocol Buffers',
        }
        return language_map.get(extension.lower(), 'Unknown')
