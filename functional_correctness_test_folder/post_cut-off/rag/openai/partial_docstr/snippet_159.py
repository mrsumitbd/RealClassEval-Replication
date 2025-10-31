
from datetime import datetime
from typing import Dict, List, Any


class MemoryFormatter:
    """
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    """

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    @staticmethod
    def _format_timestamp(ts: Any) -> str:
        """
        Convert a timestamp (int, float, or str) to a human‑readable string.
        """
        if ts is None:
            return "N/A"
        try:
            # Assume epoch seconds if numeric
            if isinstance(ts, (int, float)):
                dt = datetime.fromtimestamp(ts)
            else:
                # Try ISO format
                dt = datetime.fromisoformat(ts)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return str(ts)

    @staticmethod
    def _safe_get(d: Dict, key: str, default: Any = None) -> Any:
        return d.get(key, default)

    # ------------------------------------------------------------------
    # Public formatting methods
    # ------------------------------------------------------------------
    def format_list_response(self, response: Dict) -> List[Dict]:
        """
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        """
        docs = self._safe_get(response, "documents", [])
        formatted = []
        for doc in docs:
            formatted.append(
                {
                    "emoji": "📄",
                    "title": self._safe_get(doc, "title", "Untitled"),
                    "id": self._safe_get(doc, "id", ""),
                    "created_at": self._format_timestamp(self._safe_get(doc, "created_at")),
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
        title = self._safe_get(content_data, "title", "Untitled")
        content = self._safe_get(content_data, "content", "")
        metadata = self._safe_get(content_data, "metadata", {})
        formatted = [
            {
                "emoji": "📄",
                "title": title,
                "id": document_id,
                "kb_id": kb_id,
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
        return [
            {
                "emoji": "✅",
                "message": f'Stored document "{title}"',
                "doc_id": doc_id,
                "kb_id": kb_id,
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
        emoji = "✅" if status.lower() == "success" else "❌"
        return [
            {
                "emoji": emoji,
                "message": f"Delete {status.lower()} for document {doc_id}",
                "doc_id": doc_id,
                "kb_id": kb_id,
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
        results = self._safe_get(response, "results", [])
        formatted = []
        for res in results:
            score = self._safe_get(res, "score", 0.0)
            if score < min_score:
                continue
            title = self._safe_get(res, "title", "Untitled")
            content = self._safe_get(res, "content", "")
            formatted.append(
                {
                    "emoji": "🔍",
                    "title": title,
                    "score": round(score, 3),
                    "content": content,
                    "document_id": self._safe_get(res, "document_id", ""),
                }
            )
        return formatted
