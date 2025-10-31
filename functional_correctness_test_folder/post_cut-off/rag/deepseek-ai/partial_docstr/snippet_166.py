
import argparse


class SearchAssistantConfig:
    """Configuration class for the Search Assistant."""

    def __init__(self, args: argparse.Namespace):
        """Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        """
        self.args = args

    def validate(self) -> None:
        """Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        if not hasattr(self.args, 'query') or not self.args.query:
            raise ValueError("Query parameter is required.")
        if hasattr(self.args, 'max_results') and self.args.max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        if hasattr(self.args, 'timeout') and self.args.timeout <= 0:
            raise ValueError("timeout must be a positive number.")
