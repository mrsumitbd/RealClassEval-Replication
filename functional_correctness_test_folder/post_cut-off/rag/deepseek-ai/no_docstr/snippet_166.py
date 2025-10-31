
import argparse


class SearchAssistantConfig:
    """Configuration class for the Search Assistant."""

    def __init__(self, args: argparse.Namespace):
        """Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        """
        self.index_path = args.index_path
        self.query = args.query
        self.top_k = args.top_k
        self.threshold = args.threshold
        self.output_path = args.output_path
        self.verbose = args.verbose

    def validate(self) -> None:
        """Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        if not self.index_path:
            raise ValueError("Index path must be specified.")
        if not self.query:
            raise ValueError("Query must be specified.")
        if self.top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if not (0 <= self.threshold <= 1):
            raise ValueError("threshold must be between 0 and 1.")
