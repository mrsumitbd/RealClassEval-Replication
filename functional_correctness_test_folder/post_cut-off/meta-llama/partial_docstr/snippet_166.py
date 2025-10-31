
import argparse


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.index_name = args.index_name
        self.query = args.query
        self.top_k = args.top_k
        self.search_type = args.search_type

    def validate(self) -> None:
        '''Validate the configuration.
        Raises:
            ValueError: If the configuration is invalid.
        '''
        if not isinstance(self.index_name, str) or not self.index_name.strip():
            raise ValueError("Index name must be a non-empty string")

        if not isinstance(self.query, str) or not self.query.strip():
            raise ValueError("Query must be a non-empty string")

        if not isinstance(self.top_k, int) or self.top_k <= 0:
            raise ValueError("Top K must be a positive integer")

        if self.search_type not in ['exact', 'fuzzy']:
            raise ValueError("Search type must be either 'exact' or 'fuzzy'")
