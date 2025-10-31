from air.knowledge.document_processing_client import DocumentProcessingClient

class KnowledgeClient:
    """
    Synchronous client for knowledge services, including document processing.
    """

    def __init__(self, base_url: str, api_key: str, default_headers: dict[str, str] | None=None):
        """
        Initialize the sync knowledge client.

        Args:
            base_url (str): API base URL.
            api_key (str): API key for authentication.
            default_headers (dict, optional): Additional headers.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.default_headers = default_headers
        self.document_processing = DocumentProcessingClient(base_url=self.base_url)

    def get_graph(self):
        """
        Knowledge Graph is not supported in sync mode.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError('Knowledge Graph is only available in asynchronous mode. Use AsyncKnowledgeClient instead.')