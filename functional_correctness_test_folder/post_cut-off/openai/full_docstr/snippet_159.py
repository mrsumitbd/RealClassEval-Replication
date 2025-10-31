
from typing import Dict, List, Any


class MemoryFormatter:
    """
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    """

    # Emoji constants
    _EMOJI_LIST = "📄"
    _EMOJI_GET = "📁"
    _EMOJI_STORE = "📦"
    _EMOJI_DELETE = "❌"
    _EMOJI_RETRIEVE = "🔍"

    def format_list_response(self, response: Dict) -> List[Dict]:
        """
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        """
        documents = response.get("documents", [])
        formatted = []
        for doc in documents:
            formatted.append(
                {
                    "emoji": self._EMOJI_LIST,
                    "id": doc.get("id"),
                    "title": doc.get("title"),
                    "created_at": doc.get("created_at"),
                }
            )
        return formatted

    def format_get_response(
        self, document_id: str, kb_id: str, content_data: Dict
    ) -> List[Dict]:
        """
        Format get document response.
        Args:
            document_id: ID of the retrieved document
            kb_id: Knowledge Base ID
            content_data: Parsed content data from the document
        Returns:
            List of formatted content dictionaries for display
        """
        title = content_data.get("title", "Untitled")
        content = content_data.get("content", "")
        metadata = content_data.get("metadata", {})
        return [
            {
                "emoji": self._EMOJI_GET,
                "id": document_id,
                "kb_id": kb_id,
                "title": title,
                "content": content,
                "metadata": metadata,
            }
        ]

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        """
        Format store document response.
        Args:
            doc_id: ID of the newly stored document
            kb_id: Knowledge Base ID
            title: Title of the stored document
        Returns:
            List of formatted content dictionaries for display
        """
        return [
            {
                "emoji": self._EMOJI_STORE,
                "id": doc_id,
                "kb_id": kb_id,
                "title": title,
                "status": "stored",
            }
        ]

    def format_delete_response(
        self, status: str, doc_id: str, kb_id: str
    ) -> List[Dict]:
        """
        Format delete document response.
        Args:
            status: Status of the deletion operation
            doc_id: ID of the deleted document
            kb_id: Knowledge Base ID
        Returns:
            List of formatted content dictionaries for display
        """
        return [
            {
                "emoji": self._EMOJI_DELETE,
                "id": doc_id,
                "kb_id": kb_id,
                "status": status,
            }
        ]

    def format_retrieve_response(
        self, response: Dict, min_score: float = 0.0
    ) -> List[Dict]:
        """
        Format retrieve response.
        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results
        Returns:
            List of formatted content dictionaries for display
        """
        results = response.get("results", [])
        formatted = []
        for res in results:
            score = res.get("score", 0.0)
            if score < min_score:
                continue
            formatted.append(
                {
                    "emoji": self._EMOJI_RETRIEVE,
                    "document_id": res.get("document_id"),
                    "score": score,
                    "content": res.get("content", ""),
                }
            )
        return formatted
