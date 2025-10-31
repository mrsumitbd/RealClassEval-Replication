
from datetime import datetime
from typing import Dict, List, Any


class MemoryFormatter:
    """
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    """

    # Emoji constants
    _EMOJI_DOCUMENT = "📄"
    _EMOJI_SUCCESS = "✅"
    _EMOJI_ERROR = "❌"
    _EMOJI_RETRIEVE = "🔍"

    def _format_timestamp(self, ts: Any) -> str:
        """Convert a timestamp to a human‑readable string."""
        if ts is None:
            return "N/A"
        try:
            # Assume epoch seconds or ISO string
            if isinstance(ts, (int, float)):
                return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            return str(ts)
        except Exception:
            return str(ts)

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
                    "emoji": self._EMOJI_DOCUMENT,
                    "id": doc.get("id", "unknown"),
                    "title": doc.get("title", "Untitled"),
                    "created_at": self._format_timestamp(doc.get("created_at")),
                    "updated_at": self._format_timestamp(doc.get("updated_at")),
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
        formatted = [
            {
                "emoji": self._EMOJI_DOCUMENT,
                "id": document_id,
                "kb_id": kb_id,
                "title": title,
                "content": content,
                "metadata": metadata,
            }
        ]
        return formatted

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
        message = (
            f"{self._EMOJI_SUCCESS} Document '{title}' stored successfully "
            f"with ID {doc_id} in KB {kb_id}."
        )
        return [{"message": message}]

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
        if status.lower() in ("success", "deleted"):
            emoji = self._EMOJI_SUCCESS
            msg = f"Document {doc_id} deleted from KB {kb_id}."
        else:
            emoji = self._EMOJI_ERROR
            msg = f"Failed to delete document {doc_id} from KB {kb_id}. Status: {status}"
        return [{"emoji": emoji, "message": msg}]

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
            doc_id = res.get("document_id", "unknown")
            title = res.get("title", "Untitled")
            snippet = res.get("snippet", "")
            formatted.append(
                {
                    "emoji": self._EMOJI_RETRIEVE,
                    "document_id": doc_id,
                    "title": title,
                    "score": round(score, 3),
                    "snippet": snippet,
                }
            )
        if not formatted:
            formatted.append(
                {
                    "emoji": self._EMOJI_ERROR,
                    "message": f"No results found with score ≥ {min_score}.",
                }
            )
        return formatted
