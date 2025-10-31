
from typing import Optional
import contextvars


class BedrockAgentCoreContext:
    """Unified context manager for Bedrock AgentCore."""

    _workload_token: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
        "workload_token", default=None
    )
    _request_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
        "request_id", default=None
    )
    _session_id: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
        "session_id", default=None
    )

    @classmethod
    def set_workload_access_token(cls, token: str) -> None:
        """Set the workload access token for the current context."""
        cls._workload_token.set(token)

    @classmethod
    def get_workload_access_token(cls) -> Optional[str]:
        """Retrieve the workload access token for the current context."""
        return cls._workload_token.get()

    @classmethod
    def set_request_context(
        cls, request_id: str, session_id: Optional[str] = None
    ) -> None:
        """Set request-scoped identifiers."""
        cls._request_id.set(request_id)
        cls._session_id.set(session_id)

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        """Get current request ID."""
        return cls._request_id.get()

    @classmethod
    def get_session_id(cls) -> Optional[str]:
        """Get current session ID."""
        return cls._session_id.get()
