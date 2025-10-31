
import argparse


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.args = args

    def validate(self) -> None:
        if not hasattr(self.args, 'query'):
            raise ValueError("Missing required argument: 'query'")
