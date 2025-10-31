from typing import Dict, List, Any, Optional


class MemoryFormatter:
    '''
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    '''

    def format_list_response(self, response: Dict) -> List[Dict]:
        '''
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        '''
        documents = self._extract_list(response)
        if not documents:
            return [{"type": "text", "text": "🗂️ No documents found in the knowledge base."}]

        lines = ["🗂️ Knowledge Base Documents:", ""]
        for doc in documents:
            doc_id = self._first_non_empty(
                doc, ["id", "document_id", "doc_id"]) or "unknown"
            kb_id = self._first_non_empty(
                doc, ["knowledge_base_id", "kb_id", "kb"]) or "unknown"
            title = self._first_non_empty(
                doc, ["title", "name"]) or "(untitled)"
            source = self._first_non_empty(
                doc, ["source", "source_url", "uri"])
            extra = f" — {source}" if source else ""
            lines.append(f"• 📄 {title} (ID: {doc_id}, KB: {kb_id}){extra}")

        return [{"type": "text", "text": "\n".join(lines)}]

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        '''
        Format get document response.
        Args:
            document_id: ID of the retrieved document
            kb_id: Knowledge Base ID
            content_data: Parsed content data from the document
        Returns:
            List of formatted content dictionaries for display
        '''
        title = self._first_non_empty(
            content_data, ["title", "name"]) or "(untitled)"
        text = self._first_non_empty(
            content_data, ["text", "content", "body"]) or ""
        if not text and isinstance(content_data.get("pages"), list):
            text = "\n\n".join([self._safe_str(p.get("text") or p.get(
                "content")) for p in content_data["pages"] if isinstance(p, dict)])
        snippet = self._truncate(text, 1200) if text else "(no content)"

        header = f"📄 Document Retrieved\n• Title: {title}\n• Document ID: {document_id}\n• Knowledge Base: {kb_id}"
        body = f"\n\n📝 Content Preview:\n{snippet}"

        blocks = [{"type": "text", "text": header + body}]

        metadata = content_data.get("metadata")
        if isinstance(metadata, dict) and metadata:
            md_lines = ["\n\n🔖 Metadata:"]
            for k, v in metadata.items():
                md_lines.append(f"• {k}: {self._safe_str(v)}")
            blocks.append({"type": "text", "text": "\n".join(md_lines)})

        return blocks

    def format_store_response(self, doc_id: str, kb_id: str, title: str) -> List[Dict]:
        '''
        Format store document response.
        Args:
            doc_id: ID of the newly stored document
            kb_id: Knowledge Base ID
            title: Title of the stored document
        Returns:
            List of formatted content dictionaries for display
        '''
        title_display = title or "(untitled)"
        text = f"✅ Document stored successfully.\n• Title: {title_display}\n• Document ID: {doc_id}\n• Knowledge Base: {kb_id}"
        return [{"type": "text", "text": text}]

    def format_delete_response(self, status: str, doc_id: str, kb_id: str) -> List[Dict]:
        '''
        Format delete document response.
        Args:
            status: Status of the deletion operation
            doc_id: ID of the deleted document
            kb_id: Knowledge Base ID
        Returns:
            List of formatted content dictionaries for display
        '''
        status_norm = (status or "").lower()
        success_states = {"succeeded", "success", "ok",
                          "deleted", "completed", "200", "204", "true"}
        success = status_norm in success_states
        emoji = "🗑️✅" if success else "🗑️❌"
        text = f"{emoji} Delete document {'succeeded' if success else 'failed'}.\n• Document ID: {doc_id}\n• Knowledge Base: {kb_id}\n• Status: {status or 'unknown'}"
        return [{"type": "text", "text": text}]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve response.
        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results
        Returns:
            List of formatted content dictionaries for display
        '''
        results = self._extract_retrievals(response)
        if not results:
            return [{"type": "text", "text": "🔍 No matching content found."}]

        filtered: List[Dict[str, Any]] = []
        for item in results:
            score = self._coerce_float(self._first_non_empty(
                item, ["score", "relevance", "similarity"]))
            if score is None or score >= min_score:
                filtered.append(item)

        if not filtered:
            return [{"type": "text", "text": f"🔍 No results with score ≥ {min_score:.2f}."}]

        lines = [f"🔍 Retrieved Results (min score: {min_score:.2f}):", ""]
        for i, item in enumerate(filtered, start=1):
            title = self._first_non_empty(
                item, ["title", "document_title"]) or "(untitled)"
            doc_id = self._first_non_empty(
                item, ["document_id", "doc_id", "id"]) or "unknown"
            kb_id = self._first_non_empty(
                item, ["knowledge_base_id", "kb_id", "kb"]) or "unknown"
            score = self._coerce_float(self._first_non_empty(
                item, ["score", "relevance", "similarity"]))
            emoji = self._score_emoji(score)
            score_txt = f"{score:.3f}" if isinstance(score, float) else "n/a"
            text = self._first_non_empty(
                item, ["text", "content", "chunk", "snippet"]) or ""
            snippet = self._truncate(self._single_line(
                text), 280) if text else "(no snippet)"
            lines.append(
                f"{i}. {emoji} {title} — {snippet}\n   • Score: {score_txt} • Doc: {doc_id} • KB: {kb_id}")

        return [{"type": "text", "text": "\n".join(lines)}]

    # Helpers

    def _extract_list(self, response: Any) -> List[Dict[str, Any]]:
        if isinstance(response, list):
            return [x for x in response if isinstance(x, dict)]
        if isinstance(response, dict):
            for key in ("documents", "items", "results", "data", "records"):
                val = response.get(key)
                if isinstance(val, list):
                    return [x for x in val if isinstance(x, dict)]
        return []

    def _extract_retrievals(self, response: Any) -> List[Dict[str, Any]]:
        if isinstance(response, list):
            return [x for x in response if isinstance(x, dict)]
        if isinstance(response, dict):
            for key in ("results", "items", "matches", "documents", "data", "chunks", "retrievals"):
                val = response.get(key)
                if isinstance(val, list):
                    return [x for x in val if isinstance(x, dict)]
            # Some APIs nest under response["data"]["results"]
            data = response.get("data")
            if isinstance(data, dict):
                for key in ("results", "items", "matches", "documents", "chunks"):
                    val = data.get(key)
                    if isinstance(val, list):
                        return [x for x in val if isinstance(x, dict)]
        return []

    def _first_non_empty(self, d: Dict[str, Any], keys: List[str], default: Optional[Any] = None) -> Any:
        for k in keys:
            if k in d and d[k] not in (None, "", []):
                return d[k]
        return default

    def _truncate(self, s: str, limit: int) -> str:
        if s is None:
            return ""
        if len(s) <= limit:
            return s
        return s[: max(0, limit - 1)].rstrip() + "…"

    def _single_line(self, s: str) -> str:
        return " ".join((s or "").split())

    def _safe_str(self, v: Any) -> str:
        try:
            return str(v)
        except Exception:
            return "(unprintable)"

    def _coerce_float(self, v: Any) -> Optional[float]:
        try:
            if v is None:
                return None
            return float(v)
        except (TypeError, ValueError):
            return None

    def _score_emoji(self, score: Optional[float]) -> str:
        if score is None:
            return "⚪"
        if score >= 0.85:
            return "🟢"
        if score >= 0.65:
            return "🟡"
        if score >= 0.35:
            return "🟠"
        return "🔴"
