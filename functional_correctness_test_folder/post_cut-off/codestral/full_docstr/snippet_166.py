
import argparse


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.args = args

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if not hasattr(self.args, 'search_engine'):
            raise ValueError("Search engine not specified.")
        if not isinstance(self.args.search_engine, str):
            raise ValueError("Search engine must be a string.")
        if not hasattr(self.args, 'api_key'):
            raise ValueError("API key not specified.")
        if not isinstance(self.args.api_key, str):
            raise ValueError("API key must be a string.")
