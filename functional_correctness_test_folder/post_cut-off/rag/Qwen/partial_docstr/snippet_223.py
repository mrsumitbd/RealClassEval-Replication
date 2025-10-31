
import threading
from typing import Optional


class BedrockAgentCoreContext:
    '''Unified context manager for Bedrock AgentCore.'''
    _context = threading.local()

    @classmethod
    def set_workload_access_token(cls, token: str):
        '''Set the workload access token in the context.'''
        cls._context.workload_access_token = token

    @classmethod
    def get_workload_access_token(cls) -> Optional[str]:
        '''Get the workload access token from the context.'''
        return getattr(cls._context, 'workload_access_token', None)

    @classmethod
    def set_request_context(cls, request_id: str, session_id: Optional[str] = None):
        '''Set request-scoped identifiers.'''
        cls._context.request_id = request_id
        cls._context.session_id = session_id

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        '''Get current request ID.'''
        return getattr(cls._context, 'request_id', None)

    @classmethod
    def get_session_id(cls) -> Optional[str]:
        '''Get current session ID.'''
        return getattr(cls._context, 'session_id', None)
