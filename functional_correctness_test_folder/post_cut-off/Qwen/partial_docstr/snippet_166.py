
import argparse


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.query = args.query
        self.max_results = args.max_results
        self.source = args.source
        self.verbose = args.verbose

    def validate(self) -> None:
        if not isinstance(self.query, str) or not self.query:
            raise ValueError("Query must be a non-empty string.")
        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError("Max results must be a positive integer.")
        if not isinstance(self.source, str) or not self.source:
            raise ValueError("Source must be a non-empty string.")
        if not isinstance(self.verbose, bool):
            raise ValueError("Verbose must be a boolean.")
