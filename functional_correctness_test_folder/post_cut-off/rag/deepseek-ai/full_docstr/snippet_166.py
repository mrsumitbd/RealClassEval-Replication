
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
        if not hasattr(self.args, 'index_name'):
            raise ValueError("Missing required argument: 'index_name'")
        if not isinstance(self.args.index_name, str):
            raise ValueError("'index_name' must be a string")
        if hasattr(self.args, 'max_results') and self.args.max_results <= 0:
            raise ValueError("'max_results' must be a positive integer")
