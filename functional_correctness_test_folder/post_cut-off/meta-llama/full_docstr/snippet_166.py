
import argparse


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        self.num_results = args.num_results
        self.query = args.query
        self.search_engine = args.search_engine
        self.verbose = args.verbose

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        if not isinstance(self.num_results, int) or self.num_results <= 0:
            raise ValueError("num_results must be a positive integer")
        if not isinstance(self.query, str) or not self.query.strip():
            raise ValueError("query must be a non-empty string")
        if not isinstance(self.search_engine, str) or self.search_engine not in ['google', 'bing']:
            raise ValueError("search_engine must be either 'google' or 'bing'")
        if not isinstance(self.verbose, bool):
            raise ValueError("verbose must be a boolean")


# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Assistant')
    parser.add_argument('--num_results', type=int,
                        default=10, help='Number of search results')
    parser.add_argument('--query', type=str,
                        required=True, help='Search query')
    parser.add_argument('--search_engine', type=str, default='google',
                        choices=['google', 'bing'], help='Search engine')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose mode')
    args = parser.parse_args()
    config = SearchAssistantConfig(args)
    try:
        config.validate()
        print("Configuration is valid")
    except ValueError as e:
        print(f"Invalid configuration: {e}")
