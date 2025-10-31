import argparse
import os


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.query = getattr(args, 'query', None)
        self.index_path = getattr(args, 'index_path', None)
        self.top_k = getattr(args, 'top_k', 5)
        self.model_name = getattr(args, 'model_name', 'default-model')
        self.verbose = getattr(args, 'verbose', False)
        self.output_file = getattr(args, 'output_file', None)
        self.use_gpu = getattr(args, 'use_gpu', False)
        self.language = getattr(args, 'language', 'en')
        self.max_length = getattr(args, 'max_length', 512)
        self.min_score = getattr(args, 'min_score', 0.0)

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if not self.query or not isinstance(self.query, str):
            raise ValueError("Query must be a non-empty string.")
        if not self.index_path or not isinstance(self.index_path, str):
            raise ValueError("Index path must be a non-empty string.")
        if not os.path.exists(self.index_path):
            raise ValueError(f"Index path does not exist: {self.index_path}")
        if not isinstance(self.top_k, int) or self.top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if not isinstance(self.model_name, str) or not self.model_name:
            raise ValueError("model_name must be a non-empty string.")
        if not isinstance(self.verbose, bool):
            raise ValueError("verbose must be a boolean.")
        if self.output_file is not None and not isinstance(self.output_file, str):
            raise ValueError("output_file must be a string or None.")
        if not isinstance(self.use_gpu, bool):
            raise ValueError("use_gpu must be a boolean.")
        if not isinstance(self.language, str) or not self.language:
            raise ValueError("language must be a non-empty string.")
        if not isinstance(self.max_length, int) or self.max_length <= 0:
            raise ValueError("max_length must be a positive integer.")
        if not isinstance(self.min_score, (int, float)) or not (0.0 <= self.min_score <= 1.0):
            raise ValueError("min_score must be a float between 0.0 and 1.0.")
