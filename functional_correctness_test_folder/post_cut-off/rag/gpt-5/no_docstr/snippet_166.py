import argparse
import os
from pathlib import Path
from typing import List, Optional


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        # Paths and indexing
        self.index_path: Optional[Path] = None
        index_path_val = getattr(args, 'index_path', None)
        if index_path_val:
            self.index_path = Path(index_path_val).expanduser().resolve()
        self.data_dir: Optional[Path] = None
        data_dir_val = getattr(args, 'data_dir', None)
        if data_dir_val:
            self.data_dir = Path(data_dir_val).expanduser().resolve()
        self.index_type: str = getattr(args, 'index_type', 'faiss')

        # Model and generation
        self.provider: str = getattr(args, 'provider', 'openai')
        self.model_name: str = getattr(args, 'model_name', 'gpt-3.5-turbo')
        self.embedding_model: Optional[str] = getattr(
            args, 'embedding_model', None)
        self.temperature: float = float(getattr(args, 'temperature', 0.2))
        self.top_p: float = float(getattr(args, 'top_p', 1.0))
        self.max_tokens: int = int(getattr(args, 'max_tokens', 512))

        # Retrieval
        self.top_k: int = int(getattr(args, 'top_k', 5))
        self.similarity_threshold: float = float(
            getattr(args, 'similarity_threshold', 0.0))
        self.include_sources: bool = bool(
            getattr(args, 'include_sources', True))

        # Conversation
        self.max_history: int = int(getattr(args, 'max_history', 5))
        self.system_prompt: Optional[str] = getattr(
            args, 'system_prompt', None)

        # Networking/runtime
        self.host: str = getattr(args, 'host', '127.0.0.1')
        self.port: int = int(getattr(args, 'port', 8000))
        self.timeout: float = float(getattr(args, 'timeout', 60.0))
        self.debug: bool = bool(getattr(args, 'debug', False))
        self.verbose: bool = bool(getattr(args, 'verbose', False))
        self.log_level: str = str(getattr(args, 'log_level', 'INFO')).upper()

        # External access
        self.allow_internet: bool = bool(
            getattr(args, 'allow_internet', False))
        self.allowed_domains: List[str] = self._parse_list(
            getattr(args, 'allowed_domains', []))
        self.stop_words: List[str] = self._parse_list(
            getattr(args, 'stop_words', []))

        # Auth
        self.api_key_env: str = getattr(args, 'api_key_env', 'OPENAI_API_KEY')
        provided_api_key = getattr(args, 'api_key', None)
        self.api_key: Optional[str] = provided_api_key or os.environ.get(
            self.api_key_env)

        # Misc
        self.use_cache: bool = bool(getattr(args, 'use_cache', True))
        self.file_glob: str = getattr(
            args, 'file_glob', '**/*.md,**/*.txt,**/*.pdf')

        self.validate()

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if not self.model_name or not isinstance(self.model_name, str):
            raise ValueError('model_name must be a non-empty string.')

        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError('temperature must be between 0.0 and 2.0.')

        if not (0.0 < self.top_p <= 1.0):
            raise ValueError('top_p must be in the interval (0.0, 1.0].')

        if self.max_tokens <= 0:
            raise ValueError('max_tokens must be a positive integer.')

        if self.top_k <= 0:
            raise ValueError('top_k must be a positive integer.')

        if not (0.0 <= self.similarity_threshold <= 1.0):
            raise ValueError(
                'similarity_threshold must be between 0.0 and 1.0.')

        if self.max_history < 0:
            raise ValueError('max_history must be >= 0.')

        if not (1 <= self.port <= 65535):
            raise ValueError('port must be in the range 1-65535.')

        if self.timeout <= 0:
            raise ValueError('timeout must be > 0.')

        valid_log_levels = {'CRITICAL', 'ERROR',
                            'WARNING', 'INFO', 'DEBUG', 'NOTSET'}
        if self.log_level not in valid_log_levels:
            raise ValueError(
                f'log_level must be one of {sorted(valid_log_levels)}.')

        valid_index_types = {'faiss', 'chroma', 'annoy', 'sqlite'}
        if self.index_type not in valid_index_types:
            raise ValueError(
                f'index_type must be one of {sorted(valid_index_types)}.')

        if not self.index_path and not self.data_dir:
            raise ValueError('Either index_path or data_dir must be provided.')

        if self.index_path and not self.index_path.exists():
            raise ValueError(f'index_path does not exist: {self.index_path}')

        if self.data_dir and not self.data_dir.exists():
            raise ValueError(f'data_dir does not exist: {self.data_dir}')

        if self.provider.lower() == 'openai' and not self.api_key:
            raise ValueError(
                f'API key is required for provider "openai"; set --api_key or environment variable {self.api_key_env}.')

        if not self.allow_internet and self.allowed_domains:
            raise ValueError(
                'allowed_domains specified but allow_internet is False.')

    @staticmethod
    def _parse_list(value) -> List[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        if isinstance(value, str):
            parts = [p.strip() for p in value.split(',')]
            return [p for p in parts if p]
        return []
