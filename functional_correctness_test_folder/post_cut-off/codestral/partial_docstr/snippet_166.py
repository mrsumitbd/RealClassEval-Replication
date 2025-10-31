
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
            raise ValueError("Query argument is missing")
        if not isinstance(self.args.query, str):
            raise TypeError("Query must be a string")
        if not self.args.query.strip():
            raise ValueError("Query cannot be empty or whitespace")
