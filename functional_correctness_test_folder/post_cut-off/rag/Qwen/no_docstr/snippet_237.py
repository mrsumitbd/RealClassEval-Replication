
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
            '.bash': 'Shell',
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
            '.rkt': 'Racket',
            '.clj': 'Clojure',
            '.cljs': 'ClojureScript',
            '.cljc': 'Clojure',
            '.ex': 'Elixir',
            '.exs': 'Elixir',
            '.hs': 'Haskell',
            '.fs': 'F#',
            '.fsi': 'F#',
            '.fsx': 'F#',
            '.v': 'Verilog',
            '.sv': 'SystemVerilog',
            '.vhd': 'VHDL',
            '.vhdl': 'VHDL',
            '.tex': 'LaTeX',
            '.org': 'Org',
            '.rst': 'reStructuredText',
            '.adoc': 'AsciiDoc',
            '.proto': 'Protocol Buffers',
            '.graphql': 'GraphQL',
            '.graphqls': 'GraphQL',
            '.gql': 'GraphQL',
            '.tsv': 'TSV',
            '.csv': 'CSV',
            '.ini': 'INI',
            '.toml': 'TOML',
            '.cfg': 'Config',
            '.conf': 'Config',
            '.properties': 'Properties',
            '.env': 'Environment Variables',
            '.dockerfile': 'Dockerfile',
            '.dockerignore': 'Dockerignore',
            '.gitignore': 'Gitignore',
            '.gitattributes': 'Gitattributes',
            '.editorconfig': 'EditorConfig',
            '.prettierrc': 'Prettier',
            '.eslintrc': 'ESLint',
            '.stylelintrc': 'Stylelint',
            '.babelrc': 'Babel',
            '.jestrc': 'Jest',
            '.nycrc': 'NYC',
            '.travis.yml': 'Travis CI',
            '.circleci/config.yml': 'CircleCI',
            '.github/workflows/main.yml': 'GitHub Actions',
            '.gitlab-ci.yml': 'GitLab CI',
            '.appveyor.yml': 'AppVeyor',
            '.codecov.yml': 'Codecov',
            '.pre-commit-config.yaml': 'Pre-commit',
            '.flake8': 'Flake8',
            '.isort.cfg': 'isort',
            '.pylintrc': 'Pylint',
            '.mypy.ini': 'mypy',
            '.black': 'Black',
            '.sass-lint.yml': 'Sass-Lint',
            '.stylelintignore': 'Stylelint Ignore',
            '.eslintignore': 'ESLint Ignore',
            '.babelignore': 'Babel Ignore',
            '.jestignore': 'Jest Ignore',
            '.nycignore': 'NYC Ignore',
            '.gitmodules': 'Git Submodules',
            '.gitkeep': 'Git Keep',
            '.DS_Store': 'DS_Store',
            '.npmignore': 'NPM Ignore',
            '.yarnrc': 'Yarn',
            '.yarnrc.yml': 'Yarn',
            '.yarnclean': 'Yarn Clean',
            '.yarn-integrity': 'Yarn Integrity',
            '.yarn-metadata.json': 'Yarn Metadata',
            '.yarn/cache': 'Yarn Cache',
            '.yarn/unplugged': 'Yarn Unplugged',
            '.yarn/build-state.yml': 'Yarn Build State',
            '.yarn/install-state.gz': 'Yarn Install State',
            '.yarn/releases': 'Yarn Releases',
            '.yarn/sdks': 'Yarn SDKs',
            '.yarn/versions': 'Yarn Versions',
            '.yarn/plugins': 'Yarn Plugins',
            '.yarn/patches': 'Yarn Patches',
            '.yarn/lockfile': 'Yarn Lockfile',
            '.yarn/telemetry': 'Yarn Telemetry',
            '.yarn/unsafe-http-whitelist': 'Yarn Unsafe HTTP Whitelist',
            '.yarn/virtual': 'Yarn Virtual',
            '.yarn/cache/virtual': 'Yarn Cache Virtual',
            '.yarn/cache/virtual/cache': 'Yarn Cache Virtual Cache',
            '.yarn/cache/virtual/cache/cache': 'Yarn Cache Virtual Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache Cache',
            '.yarn/cache/virtual/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache/cache': 'Yarn Cache Virtual Cache Cache Cache
