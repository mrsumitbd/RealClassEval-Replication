
import argparse
from typing import List


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.index_path = args.index_path
        self.query = args.query
        self.top_k = args.top_k
        self.embedding_model = args.embedding_model
        self.device = args.device

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if not self.index_path:
            raise ValueError("Index path must be provided.")
        if not self.query:
            raise ValueError("Query must be provided.")
        if self.top_k <= 0:
            raise ValueError("Top k must be a positive integer.")
        if not self.embedding_model:
            raise ValueError("Embedding model must be specified.")
        if self.device not in ['cpu', 'cuda']:
            raise ValueError("Device must be either 'cpu' or 'cuda'.")
