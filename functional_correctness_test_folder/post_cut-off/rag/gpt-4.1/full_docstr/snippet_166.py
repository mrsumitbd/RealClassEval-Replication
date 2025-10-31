import argparse
import os


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.index_path = getattr(args, 'index_path', None)
        self.data_path = getattr(args, 'data_path', None)
        self.model_name = getattr(args, 'model_name', 'all-MiniLM-L6-v2')
        self.top_k = getattr(args, 'top_k', 5)
        self.device = getattr(args, 'device', 'cpu')
        self.verbose = getattr(args, 'verbose', False)
        self.save_index = getattr(args, 'save_index', False)
        self.load_index = getattr(args, 'load_index', False)
        self.query = getattr(args, 'query', None)
        self.batch_size = getattr(args, 'batch_size', 32)
        self.max_length = getattr(args, 'max_length', 512)

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if self.index_path is not None and not isinstance(self.index_path, str):
            raise ValueError("index_path must be a string or None.")
        if self.data_path is not None and not isinstance(self.data_path, str):
            raise ValueError("data_path must be a string or None.")
        if self.index_path is not None and self.save_index:
            index_dir = os.path.dirname(self.index_path)
            if index_dir and not os.path.exists(index_dir):
                raise ValueError(
                    f"Directory for index_path does not exist: {index_dir}")
        if self.data_path is not None and not os.path.exists(self.data_path):
            raise ValueError(f"data_path does not exist: {self.data_path}")
        if not isinstance(self.model_name, str) or not self.model_name:
            raise ValueError("model_name must be a non-empty string.")
        if not isinstance(self.top_k, int) or self.top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if self.device not in ['cpu', 'cuda']:
            raise ValueError("device must be 'cpu' or 'cuda'.")
        if not isinstance(self.verbose, bool):
            raise ValueError("verbose must be a boolean.")
        if not isinstance(self.save_index, bool):
            raise ValueError("save_index must be a boolean.")
        if not isinstance(self.load_index, bool):
            raise ValueError("load_index must be a boolean.")
        if self.query is not None and not isinstance(self.query, str):
            raise ValueError("query must be a string or None.")
        if not isinstance(self.batch_size, int) or self.batch_size <= 0:
            raise ValueError("batch_size must be a positive integer.")
        if not isinstance(self.max_length, int) or self.max_length <= 0:
            raise ValueError("max_length must be a positive integer.")
        if self.load_index and (self.index_path is None or not os.path.exists(self.index_path)):
            raise ValueError("index_path must exist if load_index is True.")
