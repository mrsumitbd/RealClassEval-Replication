from typing import Dict, List, Any, Optional


class MemoryFormatter:
    def _normalize_list(self, response: Any) -> List[Dict]:
        if response is None:
            return []
        if isinstance(response, list):
            return [x for x in response if isinstance(x, dict)]
        if isinstance(response, dict):
            for key in ("documents", "items", "results", "matches", "data", "hits"):
                if key in response and isinstance(response[key], list):
                    return [x for x in response[key] if isinstance(x, dict)]
            return [response]
        return []

    def _get_first(self, d: Dict, *keys, default=None):
        for k in keys:
            if k in d and d[k] is not None:
                return d[k]
        return default

    def _extract_ids(self, item: Dict, fallback_kb_id: Optional[str] = None, fallback_doc_id: Optional[str] = None):
        doc = self._get_first(item, "document", "doc", default={}) or {}
        meta = self._get_first(item, "metadata", "meta", default={}) or {}

        document_id = (
            self._get_first(
                item,
                "document_id",
                "doc_id",
                "id",
                default=None,
            )
            or self._get_first(doc, "document_id", "doc_id", "id", default=None)
            or self._get_first(meta, "document_id", "doc_id", "id", default=None)
            or fallback_doc_id
        )
        kb_id = (
            self._get_first(
                item,
                "kb_id",
                "knowledge_base_id",
                "kb",
                default=None,
            )
            or self._get_first(doc, "kb_id", "knowledge_base_id", "kb", default=None)
            or self._get_first(meta, "kb_id", "knowledge_base_id", "kb", default=None)
            or fallback_kb_id
        )
        return document_id, kb_id

    def _extract_title(self, item: Dict) -> Optional[str]:
        meta = item.get("metadata") or {}
        return self._get_first(item, "title", "name", default=None) or self._get_first(meta, "title", "name", default=None)

    def _extract_content(self, item: Dict) -> Optional[str]:
        return self._get_first(
            item,
            "content",
            "text",
            "page_content",
            "chunk",
            "snippet",
            "body",
            default=None,
        )

    def _extract_chunks(self, item: Dict) -> List[Any]:
        chunks = self._get_first(
            item, "chunks", "segments", "pages", default=[])
        return chunks if isinstance(chunks, list) else []

    def _extract_score(self, item: Dict) -> Optional[float]:
        score = self._get_first(
            item, "score", "similarity", "relevance", default=None)
        try:
            return float(score) if score is not None else None
        except (TypeError, ValueError):
            return None

    def _extract_metadata(self, item: Dict) -> Dict:
        meta = self._get_first(item, "metadata", "meta", default={}) or {}
        return meta if isinstance(meta, dict) else {}

    def _extract_chunk_id(self, item: Dict) -> Optional[str]:
        return self._get_first(item, "chunk_id", "part_id", "section_id", default=None)

    def format_list_response(self, response: Dict) -> List[Dict]:
        items = self._normalize_list(response)
        fallback_kb_id = None
        if isinstance(response, dict):
            fallback_kb_id = self._get_first(
                response, "kb_id", "knowledge_base_id", "kb", default=None)

        formatted = []
        for it in items:
            document_id, kb_id = self._extract_ids(
                it, fallback_kb_id=fallback_kb_id)
            formatted.append(
                {
                    "kb_id": kb_id,
                    "document_id": document_id,
                    "title": self._extract_title(it),
                    "status": self._get_first(it, "status", "state", default=None),
                    "created_at": self._get_first(it, "created_at", "created", default=None),
                    "updated_at": self._get_first(it, "updated_at", "updated", default=None),
                    "metadata": self._extract_metadata(it),
                }
            )
        return formatted

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        content = self._extract_content(content_data or {}) or ""
        chunks = self._extract_chunks(content_data or {})
        title = self._extract_title(content_data or {}) or ""
        metadata = self._extract_metadata(content_data or {})
        chunk_id = self._extract_chunk_id(content_data or {})

        return [
            {
                "kb_id": kb_id,
                "document_id": document_id,
                "title": title,
                "content": content,
                "chunks": chunks,
                "chunk_id": chunk_id,
                "metadata": metadata,
            }
        ]

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        return [
            {
                "status": "stored",
                "kb_id": kb_id,
                "document_id": doc_id,
                "title": title,
            }
        ]

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        norm_status = (status or "").strip().lower()
        if norm_status in ("ok", "success", "successful", "true", "1"):
            norm_status = "deleted"
        elif not norm_status:
            norm_status = "deleted"
        return [
            {
                "status": norm_status,
                "kb_id": kb_id,
                "document_id": doc_id,
            }
        ]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        items = self._normalize_list(response)
        fallback_kb_id = None
        if isinstance(response, dict):
            fallback_kb_id = self._get_first(
                response, "kb_id", "knowledge_base_id", "kb", default=None)

        results: List[Dict] = []
        for it in items:
            score = self._extract_score(it)
            if score is not None and score < float(min_score):
                continue

            document_id, kb_id = self._extract_ids(
                it, fallback_kb_id=fallback_kb_id)
            results.append(
                {
                    "content": self._extract_content(it),
                    "score": score,
                    "kb_id": kb_id,
                    "document_id": document_id,
                    "chunk_id": self._extract_chunk_id(it),
                    "title": self._extract_title(it),
                    "metadata": self._extract_metadata(it),
                }
            )
        return results
