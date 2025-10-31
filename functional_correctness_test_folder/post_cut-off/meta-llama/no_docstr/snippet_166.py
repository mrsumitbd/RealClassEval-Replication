
import argparse


class SearchAssistantConfig:

    def __init__(self, args: argparse.Namespace):
        self.search_engine = args.search_engine
        self.max_results = args.max_results
        self.timeout = args.timeout
        self.user_agent = args.user_agent

    def validate(self) -> None:
        if not hasattr(self, 'search_engine') or self.search_engine is None:
            raise ValueError("Search engine must be specified")
        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError("Max results must be a positive integer")
        if not isinstance(self.timeout, (int, float)) or self.timeout <= 0:
            raise ValueError("Timeout must be a positive number")
        if not isinstance(self.user_agent, str) or len(self.user_agent.strip()) == 0:
            raise ValueError("User agent must be a non-empty string")


# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Assistant Config')
    parser.add_argument('--search_engine', type=str,
                        help='Search engine to use')
    parser.add_argument('--max_results', type=int, default=10,
                        help='Maximum number of results to return')
    parser.add_argument('--timeout', type=float,
                        default=5.0, help='Timeout in seconds')
    parser.add_argument('--user_agent', type=str,
                        default='SearchAssistant/1.0', help='User agent string')

    args = parser.parse_args(['--search_engine', 'google'])
    config = SearchAssistantConfig(args)
    config.validate()
