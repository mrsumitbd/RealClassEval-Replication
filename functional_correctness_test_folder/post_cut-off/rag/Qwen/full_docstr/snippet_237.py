
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
            '.sh': 'Shell',
            '.go': 'Go',
            '.ts': 'TypeScript',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.rs': 'Rust',
            '.pl': 'Perl',
            '.r': 'R',
            '.m': 'Objective-C',
            '.sql': 'SQL',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.c': 'C',
            '.h': 'C',
            '.cs': 'C#',
            '.vue': 'Vue.js',
            '.tsx': 'TypeScript React',
            '.jsx': 'JavaScript React',
            '.dart': 'Dart',
            '.tsv': 'TSV',
            '.csv': 'CSV',
            '.graphql': 'GraphQL',
            '.proto': 'Protocol Buffers',
            '.graphqls': 'GraphQL Schema',
            '.graphqlql': 'GraphQL',
            '.gql': 'GraphQL',
            '.gqls': 'GraphQL Schema',
            '.svelte': 'Svelte',
            '.ts': 'TypeScript',
            '.coffee': 'CoffeeScript',
            '.hs': 'Haskell',
            '.erl': 'Erlang',
            '.ex': 'Elixir',
            '.exs': 'Elixir Script',
            '.jl': 'Julia',
            '.clj': 'Clojure',
            '.cljc': 'Clojure',
            '.cljs': 'ClojureScript',
            '.edn': 'EDN',
            '.fs': 'F#',
            '.fsi': 'F# Interactive',
            '.fsx': 'F# Script',
            '.fsscript': 'F# Script',
            '.fsproj': 'F# Project',
            '.hs': 'Haskell',
            '.lhs': 'Literate Haskell',
            '.lua': 'Lua',
            '.nim': 'Nim',
            '.nims': 'Nim Script',
            '.nim.cfg': 'Nim Config',
            '.rkt': 'Racket',
            '.scm': 'Scheme',
            '.ss': 'Scheme',
            '.rktl': 'Racket',
            '.rktu': 'Racket Unit',
            '.rktm': 'Racket Module',
            '.d': 'D',
            '.coffee': 'CoffeeScript',
            '.litcoffee': 'Literate CoffeeScript',
            '.iced': 'IcedCoffeeScript',
            '.toml': 'TOML',
            '.lock': 'Lockfile',
            '.dockerfile': 'Dockerfile',
            '.dockerignore': 'Docker Ignore',
            '.gitignore': 'Git Ignore',
            '.gitattributes': 'Git Attributes',
            '.editorconfig': 'EditorConfig',
            '.prettierrc': 'Prettier Config',
            '.eslintrc': 'ESLint Config',
            '.babelrc': 'Babel Config',
            '.jestrc': 'Jest Config',
            '.nycrc': 'NYC Config',
            '.travis.yml': 'Travis CI Config',
            '.circleci': 'CircleCI Config',
            '.github': 'GitHub Config',
            '.gitlab-ci.yml': 'GitLab CI Config',
            '.appveyor.yml': 'AppVeyor Config',
            '.codecov.yml': 'Codecov Config',
            '.pre-commit-config.yaml': 'Pre-commit Config',
            '.flake8': 'Flake8 Config',
            '.isort.cfg': 'isort Config',
            '.pylintrc': 'Pylint Config',
            '.mypy.ini': 'Mypy Config',
            '.bandit': 'Bandit Config',
            '.black': 'Black Config',
            '.editorconfig': 'EditorConfig',
            '.env': 'Environment Variables',
            '.env.example': 'Environment Variables Example',
            '.env.development': 'Development Environment Variables',
            '.env.production': 'Production Environment Variables',
            '.env.test': 'Test Environment Variables',
            '.env.local': 'Local Environment Variables',
            '.env.test.local': 'Local Test Environment Variables',
            '.env.development.local': 'Local Development Environment Variables',
            '.env.production.local': 'Local Production Environment Variables',
        }
        return language_map.get(extension.lower(), 'Unknown')
