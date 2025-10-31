from falconpy import APIHarnessV2
import os
from importlib.metadata import PackageNotFoundError, version
import sys
from typing import Any, Dict, Optional
import platform

class FalconClient:
    """Client for interacting with the CrowdStrike Falcon API."""

    def __init__(self, base_url: Optional[str]=None, debug: bool=False, user_agent_comment: Optional[str]=None):
        """Initialize the Falcon client.

        Args:
            base_url: Falcon API base URL (defaults to FALCON_BASE_URL env var)
            debug: Enable debug logging
            user_agent_comment: Additional information to include in the User-Agent comment section
        """
        self.client_id = os.environ.get('FALCON_CLIENT_ID')
        self.client_secret = os.environ.get('FALCON_CLIENT_SECRET')
        self.base_url = base_url or os.environ.get('FALCON_BASE_URL', 'https://api.crowdstrike.com')
        self.debug = debug
        self.user_agent_comment = user_agent_comment or os.environ.get('FALCON_MCP_USER_AGENT_COMMENT')
        if not self.client_id or not self.client_secret:
            raise ValueError('Falcon API credentials not provided. Set FALCON_CLIENT_ID and FALCON_CLIENT_SECRET environment variables.')
        self.client = APIHarnessV2(client_id=self.client_id, client_secret=self.client_secret, base_url=self.base_url, debug=debug, user_agent=self.get_user_agent())
        logger.debug('Initialized Falcon client with base URL: %s', self.base_url)

    def authenticate(self) -> bool:
        """Authenticate with the Falcon API.

        Returns:
            bool: True if authentication was successful
        """
        return self.client.login()

    def is_authenticated(self) -> bool:
        """Check if the client is authenticated.

        Returns:
            bool: True if the client is authenticated
        """
        return self.client.token_valid

    def command(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute a Falcon API command.

        Args:
            operation: The API operation to execute
            **kwargs: Additional arguments to pass to the API

        Returns:
            Dict[str, Any]: The API response
        """
        return self.client.command(operation, **kwargs)

    def get_user_agent(self) -> str:
        """Get RFC-compliant user agent string for API requests.

        Returns:
            str: User agent string in RFC format "falcon-mcp/VERSION (comment; falconpy/VERSION; Python/VERSION; Platform/VERSION)"
        """
        falcon_mcp_version = get_version()
        python_version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
        platform_info = f'{platform.system()}/{platform.release()}'
        try:
            falconpy_version = version('crowdstrike-falconpy')
        except PackageNotFoundError:
            falconpy_version = 'unknown'
            logger.debug('crowdstrike-falconpy package version not found')
        comment_parts = []
        if self.user_agent_comment:
            comment_parts.append(self.user_agent_comment.strip())
        comment_parts.extend([f'falconpy/{falconpy_version}', f'Python/{python_version}', platform_info])
        return f"falcon-mcp/{falcon_mcp_version} ({'; '.join(comment_parts)})"

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests.

        This method returns the authentication headers from the underlying Falcon API client,
        which can be used for custom HTTP requests or advanced integration scenarios.

        Returns:
            Dict[str, str]: Authentication headers including the bearer token
        """
        return self.client.auth_headers