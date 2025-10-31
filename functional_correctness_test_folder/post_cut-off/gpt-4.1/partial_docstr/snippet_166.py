
import argparse
import os


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.query = getattr(args, 'query', None)
        self.data_path = getattr(args, 'data_path', None)
        self.top_k = getattr(args, 'top_k', 5)
        self.verbose = getattr(args, 'verbose', False)
        self.output = getattr(args, 'output', None)

    def validate(self) -> None:
        if not self.query or not isinstance(self.query, str):
            raise ValueError("Query must be a non-empty string.")
        if not self.data_path or not isinstance(self.data_path, str):
            raise ValueError("Data path must be a non-empty string.")
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(
                f"Data path '{self.data_path}' does not exist.")
        if not isinstance(self.top_k, int) or self.top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if self.output is not None and not isinstance(self.output, str):
            raise ValueError("Output path must be a string if specified.")
