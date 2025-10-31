
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
        self.max_results = getattr(args, 'max_results', 10)
        self.data_dir = getattr(args, 'data_dir', None)
        self.verbose = getattr(args, 'verbose', False)

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if not self.query or not isinstance(self.query, str):
            raise ValueError("Query must be a non-empty string.")
        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        if not self.data_dir or not isinstance(self.data_dir, str):
            raise ValueError("data_dir must be a non-empty string.")
        if not os.path.isdir(self.data_dir):
            raise ValueError(
                f"data_dir '{self.data_dir}' does not exist or is not a directory.")
        if not isinstance(self.verbose, bool):
            raise ValueError("verbose must be a boolean value.")
