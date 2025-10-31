from typing import Optional
from contextvars import ContextVar


class BedrockAgentCoreContext:
    _workload_access_token: ContextVar[Optional[str]] = ContextVar(
        "_workload_access_token", default=None)
    _request_id: ContextVar[Optional[str]] = ContextVar(
        "_request_id", default=None)
    _session_id: ContextVar[Optional[str]] = ContextVar(
        "_session_id", default=None)

    @classmethod
    def set_workload_access_token(cls, token: str):
        cls._workload_access_token.set(token)

    @classmethod
    def get_workload_access_token(cls) -> Optional[str]:
        return cls._workload_access_token.get()

    @classmethod
    def set_request_context(cls, request_id: str, session_id: Optional[str] = None):
        cls._request_id.set(request_id)
        cls._session_id.set(session_id)

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        return cls._request_id.get()

    @classmethod
    def get_session_id(cls) -> Optional[str]:
        return cls._session_id.get()
