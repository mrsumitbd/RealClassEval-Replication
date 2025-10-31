
class BedrockAgentCoreContext:
    '''Unified context manager for Bedrock AgentCore.'''
    _workload_access_token: Optional[str] = None
    _request_id: Optional[str] = None
    _session_id: Optional[str] = None

    @classmethod
    def set_workload_access_token(cls, token: str):
        '''Set the workload access token in the context.'''
        cls._workload_access_token = token

    @classmethod
    def get_workload_access_token(cls) -> Optional[str]:
        '''Get the workload access token from the context.'''
        return cls._workload_access_token

    @classmethod
    def set_request_context(cls, request_id: str, session_id: Optional[str] = None):
        '''Set request-scoped identifiers.'''
        cls._request_id = request_id
        cls._session_id = session_id

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        '''Get current request ID.'''
        return cls._request_id

    @classmethod
    def get_session_id(cls) -> Optional[str]:
        '''Get current session ID.'''
        return cls._session_id
