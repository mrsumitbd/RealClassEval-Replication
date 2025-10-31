from typing import Optional
from contextvars import ContextVar

class BedrockAgentCoreContext:
    """Unified context manager for Bedrock AgentCore."""
    _workload_access_token: ContextVar[Optional[str]] = ContextVar('workload_access_token')
    _request_id: ContextVar[Optional[str]] = ContextVar('request_id')
    _session_id: ContextVar[Optional[str]] = ContextVar('session_id')

    @classmethod
    def set_workload_access_token(cls, token: str):
        """Set the workload access token in the context."""
        cls._workload_access_token.set(token)

    @classmethod
    def get_workload_access_token(cls) -> Optional[str]:
        """Get the workload access token from the context."""
        try:
            return cls._workload_access_token.get()
        except LookupError:
            return None

    @classmethod
    def set_request_context(cls, request_id: str, session_id: Optional[str]=None):
        """Set request-scoped identifiers."""
        cls._request_id.set(request_id)
        cls._session_id.set(session_id)

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        """Get current request ID."""
        try:
            return cls._request_id.get()
        except LookupError:
            return None

    @classmethod
    def get_session_id(cls) -> Optional[str]:
        """Get current session ID."""
        try:
            return cls._session_id.get()
        except LookupError:
            return None