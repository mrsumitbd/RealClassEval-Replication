
import argparse


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        self.query = getattr(args, 'query', None)
        self.max_results = getattr(args, 'max_results', 10)
        self.language = getattr(args, 'language', 'en')
        self.verbose = getattr(args, 'verbose', False)

    def validate(self) -> None:
        if not isinstance(self.query, str) or not self.query.strip():
            raise ValueError("Query must be a non-empty string.")
        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        if not isinstance(self.language, str) or not self.language:
            raise ValueError("language must be a non-empty string.")
        if not isinstance(self.verbose, bool):
            raise ValueError("verbose must be a boolean.")
