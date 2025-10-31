
from typing import Dict, List, Any


class MemoryFormatter:
    """
    Utility class for normalising responses from a memory store.
    """

    def format_list_response(self, response: Dict) -> List[Dict]:
        """
        Normalise a list response.

        Parameters
        ----------
        response : Dict
            Raw response from the memory store. Expected to contain a key
            ``documents`` with a list of document dictionaries.

        Returns
        -------
        List[Dict]
            A list of dictionaries each containing the keys
            ``document_id``, ``kb_id`` and ``title`` (if present).
        """
        documents = response.get("documents", [])
        formatted = []
        for doc in documents:
            formatted.append(
                {
                    "document_id": doc.get("document_id") or doc.get("id"),
                    "kb_id": doc.get("kb_id"),
                    "title": doc.get("title"),
                }
            )
        return formatted

    def format_get_response(
        self, document_id: str, kb_id: str, content_data: Dict
    ) -> List[Dict]:
        """
        Normalise a get response.

        Parameters
        ----------
        document_id : str
            Identifier of the retrieved document.
        kb_id : str
            Knowledge base identifier.
        content_data : Dict
            Raw content of the document.

        Returns
        -------
        List[Dict]
            A single‑item list containing the document metadata and content.
        """
        return [
            {
                "document_id": document_id,
                "kb_id": kb_id,
                "content": content_data,
            }
        ]

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        """
        Normalise a store response.

        Parameters
        ----------
        doc_id : str
            Identifier of the stored document.
        kb_id : str
            Knowledge base identifier.
        title : str
            Title of the stored document.

        Returns
        -------
        List[Dict]
            A single‑item list containing the stored document metadata.
        """
        return [
            {
                "document_id": doc_id,
                "kb_id": kb_id,
                "title": title,
            }
        ]

    def format_delete_response(
        self, status: str, doc_id: str, kb_id: str
    ) -> List[Dict]:
        """
        Normalise a delete response.

        Parameters
        ----------
        status : str
            Status of the delete operation (e.g., "success" or "failed").
        doc_id : str
            Identifier of the deleted document.
        kb_id : str
            Knowledge base identifier.

        Returns
        -------
        List[Dict]
            A single‑item list containing the delete operation result.
        """
        return [
            {
                "status": status,
                "document_id": doc_id,
                "kb_id": kb_id,
            }
        ]

    def format_retrieve_response(
        self, response: Dict, min_score: float = 0.0
    ) -> List[Dict]:
        """
        Normalise a retrieve response.

        Parameters
        ----------
        response : Dict
            Raw response from the memory store. Expected to contain a key
            ``results`` with a list of result dictionaries.
        min_score : float, optional
            Minimum score threshold for filtering results.

        Returns
        -------
        List[Dict]
            A list of dictionaries each containing the keys
            ``document_id``, ``kb_id``, ``score`` and ``content``.
        """
        results = response.get("results", [])
        formatted = []
        for res in results:
            score = res.get("score", 0.0)
            if score < min_score:
                continue
            formatted.append(
                {
                    "document_id": res.get("document_id") or res.get("id"),
                    "kb_id": res.get("kb_id"),
                    "score": score,
                    "content": res.get("content"),
                }
            )
        return formatted
