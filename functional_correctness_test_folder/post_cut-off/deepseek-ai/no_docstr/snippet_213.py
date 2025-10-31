
class LocalBedrockAgentCoreClient:

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        pass
