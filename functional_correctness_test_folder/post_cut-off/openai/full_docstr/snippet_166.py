
import argparse
import re
from urllib.parse import urlparse


class SearchAssistantConfig:
    '''Configuration class for the Search Assistant.'''

    def __init__(self, args: argparse.Namespace):
        '''Initialize configuration from command line arguments.
        Args:
            args: Parsed command line arguments.
        '''
        # Store all arguments as attributes
        for key, value in vars(args).items():
            setattr(self, key, value)

        # Set defaults for optional parameters if not provided
        self.max_results = getattr(self, 'max_results', 10)
        self.timeout = getattr(self, 'timeout', 5.0)

    def validate(self) -> None:
        '''Validate configuration parameters.
        Raises:
            ValueError: If any configuration parameter is invalid.
        '''
        # API key must be a non-empty string
        api_key = getattr(self, 'api_key', None)
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError('api_key must be a non-empty string')

        # Search endpoint must be a valid URL
        endpoint = getattr(self, 'search_endpoint', None)
        if not isinstance(endpoint, str) or not endpoint.strip():
            raise ValueError('search_endpoint must be a non-empty string')
        parsed = urlparse(endpoint)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(
                f'search_endpoint "{endpoint}" is not a valid URL')

        # max_results must be a positive integer
        if not isinstance(self.max_results, int) or self.max_results <= 0:
            raise ValueError('max_results must be a positive integer')

        # timeout must be a positive number (int or float)
        if not isinstance(self.timeout, (int, float)) or self.timeout <= 0:
            raise ValueError('timeout must be a positive number')
