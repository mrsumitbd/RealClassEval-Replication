from typing import Optional
from contextvars import ContextVar


class BedrockAgentCoreContext:
    '''Unified context manager for Bedrock AgentCore.'''

    _workload_access_token: ContextVar[Optional[str]] = ContextVar(
        "workload_access_token", default=None)
    _request_id: ContextVar[Optional[str]] = ContextVar(
        "request_id", default=None)
    _session_id: ContextVar[Optional[str]] = ContextVar(
        "session_id", default=None)

    @classmethod
    def set_workload_access_token(cls, token: Optional[str]):
        cls._workload_access_token.set(token)

    @classmethod
    def get_workload_access_token(cls) -> Optional[str]:
        return cls._workload_access_token.get()

    @classmethod
    def set_request_context(cls, request_id: Optional[str], session_id: Optional[str] = None):
        '''Set request-scoped identifiers.'''
        cls._request_id.set(request_id)
        cls._session_id.set(session_id)

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        '''Get current request ID.'''
        return cls._request_id.get()

    @classmethod
    def get_session_id(cls) -> Optional[str]:
        return cls._session_id.get()
