
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
        if not hasattr(self.args, 'query') or not self.args.query:
            raise ValueError("Query parameter is required.")
