
import argparse
import os


class SearchAssistantConfig:
    """
    Configuration holder for the Search Assistant.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command line arguments.
    """

    def __init__(self, args: argparse.Namespace):
        # Store raw args
        self.args = args

        # Required arguments
        self.search_query = getattr(args, "search_query", None)
        self.index_path = getattr(args, "index_path", None)

        # Optional arguments with defaults
        self.top_k = getattr(args, "top_k", 10)
        self.output_file = getattr(args, "output_file", None)
        self.verbose = getattr(args, "verbose", False)

    def validate(self) -> None:
        """
        Validate the configuration.

        Raises
        ------
        ValueError
            If required arguments are missing or invalid.
        """
        if not self.search_query:
            raise ValueError("The 'search_query' argument is required.")

        if not self.index_path:
            raise ValueError("The 'index_path' argument is required.")

        if not isinstance(self.top_k, int) or self.top_k <= 0:
            raise ValueError(
                "The 'top_k' argument must be a positive integer.")

        if not os.path.exists(self.index_path):
            raise ValueError(
                f"The index path '{self.index_path}' does not exist.")
