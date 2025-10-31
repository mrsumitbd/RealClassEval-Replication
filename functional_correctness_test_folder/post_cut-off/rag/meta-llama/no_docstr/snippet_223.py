
import threading
from typing import Optional


class BedrockAgentCoreContext(threading.local):
    """Unified context manager for Bedrock AgentCore."""

    def __init__(self):
        self.workload_access_token = None
        self.request_id = None
        self.session_id = None

    @classmethod
    def _get_context(cls) -> 'BedrockAgentCoreContext':
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    @classmethod
    def set_workload_access_token(cls, token: str):
        """Set the workload access token in the context."""
        cls._get_context().workload_access_token = token

    @classmethod
    def get_workload_access_token(cls) -> Optional[str]:
        """Get the workload access token from the context."""
        return cls._get_context().workload_access_token

    @classmethod
    def set_request_context(cls, request_id: str, session_id: Optional[str] = None):
        """Set request-scoped identifiers."""
        context = cls._get_context()
        context.request_id = request_id
        context.session_id = session_id

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        """Get current request ID."""
        return cls._get_context().request_id

    @classmethod
    def get_session_id(cls) -> Optional[str]:
        """Get current session ID."""
        return cls._get_context().session_id
