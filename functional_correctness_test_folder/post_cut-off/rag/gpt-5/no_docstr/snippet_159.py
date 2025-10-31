from typing import Dict, List, Any, Optional


class MemoryFormatter:
    '''
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    '''

    def _text_item(self, text: str) -> Dict[str, str]:
        return {"type": "text", "text": text}

    def _truncate(self, text: Optional[str], limit: int = 400) -> str:
        if not text:
            return ""
        text = str(text).strip()
        return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"

    def _as_float(self, value: Any) -> Optional[float]:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _collect_docs(self, response: Dict) -> List[Dict]:
        # Try common keys where documents may be returned
        for key in ("documents", "data", "items", "results", "knowledge_base_documents"):
            docs = response.get(key)
            if isinstance(docs, list):
                return docs
        # Single object fallback
        if isinstance(response, dict) and any(k in response for k in ("id", "doc_id", "document_id")):
            return [response]
        return []

    def _get_doc_id(self, doc: Dict) -> Optional[str]:
        return doc.get("id") or doc.get("doc_id") or doc.get("document_id")

    def _get_kb_id(self, doc: Dict, default: Optional[str] = None) -> Optional[str]:
        return doc.get("knowledge_base_id") or doc.get("kb_id") or default

    def _get_title(self, doc: Dict) -> str:
        return (
            doc.get("title")
            or doc.get("name")
            or (doc.get("metadata") or {}).get("title")
            or "Untitled"
        )

    def format_list_response(self, response: Dict) -> List[Dict]:
        '''
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        '''
        output: List[Dict] = []
        docs = self._collect_docs(response or {})
        kb_id = response.get("knowledge_base_id") or response.get("kb_id")

        if not docs:
            header = "📚 No documents found."
            if kb_id:
                header = f"{header} KB: {kb_id}"
            return [self._text_item(header)]

        header = "📚 Knowledge Base Documents"
        if kb_id:
            header = f"{header} (KB: {kb_id})"
        output.append(self._text_item(header))
        output.append(self._text_item(f"Found: {len(docs)}"))

        for idx, doc in enumerate(docs, start=1):
            doc_id = self._get_doc_id(doc) or "unknown"
            title = self._get_title(doc)
            doc_kb = self._get_kb_id(doc, kb_id) or "unknown"
            source = doc.get("source") or doc.get("url")
            extra_bits = []
            if source:
                extra_bits.append(f"source: {source}")
            if doc.get("type"):
                extra_bits.append(f"type: {doc.get('type')}")
            if doc.get("status"):
                extra_bits.append(f"status: {doc.get('status')}")
            extras = f" | {'; '.join(extra_bits)}" if extra_bits else ""
            output.append(self._text_item(
                f"- {idx}. {title} — ID: {doc_id} | KB: {doc_kb}{extras}"))

        return output

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
        output: List[Dict] = []
        content_data = content_data or {}

        title = (
            content_data.get("title")
            or (content_data.get("metadata") or {}).get("title")
            or "Untitled"
        )
        summary = content_data.get("summary") or content_data.get("overview")
        headings = content_data.get(
            "headings") or content_data.get("sections") or []
        text = content_data.get("content") or content_data.get("text") or ""
        chunks = content_data.get("chunks") or []
        tokens = content_data.get("token_count") or content_data.get("tokens")

        output.append(self._text_item("📄 Document Retrieved"))
        output.append(self._text_item(f"Title: {title}"))
        output.append(self._text_item(f"ID: {document_id} | KB: {kb_id}"))

        if tokens:
            output.append(self._text_item(f"Tokens: {tokens}"))
        if chunks:
            output.append(self._text_item(f"Chunks: {len(chunks)}"))
        if headings:
            top_headings = [str(h).strip()
                            for h in headings if str(h).strip()][:5]
            if top_headings:
                output.append(self._text_item("Headings:"))
                for h in top_headings:
                    output.append(self._text_item(f"- {h}"))

        if summary:
            output.append(self._text_item("Summary:"))
            output.append(self._text_item(self._truncate(str(summary), 600)))

        if text and not summary:
            output.append(self._text_item("Content Preview:"))
            output.append(self._text_item(self._truncate(str(text), 600)))

        return output

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
        title_display = title or "Untitled"
        return [
            self._text_item("💾 Document Stored"),
            self._text_item(f"Title: {title_display}"),
            self._text_item(f"ID: {doc_id} | KB: {kb_id}"),
            self._text_item("Status: ✅ Success"),
        ]

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
        normalized = (status or "").strip().lower()
        success_values = {"success", "succeeded",
                          "ok", "deleted", "true", "completed"}
        is_success = normalized in success_values
        emoji = "🗑️" if is_success else "⚠️"
        status_line = "Deleted" if is_success else f"Delete status: {status or 'unknown'}"

        return [
            self._text_item(f"{emoji} {status_line}"),
            self._text_item(f"ID: {doc_id} | KB: {kb_id}"),
        ]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve response.
        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results
        Returns:
            List of formatted content dictionaries for display
        '''
        output: List[Dict] = []
        results = response.get("results") or response.get(
            "matches") or response.get("data") or []

        if not isinstance(results, list) or not results:
            return [self._text_item("🔎 No results found.")]

        # Filter and normalize scores
        filtered: List[Dict] = []
        for item in results:
            score = (
                self._as_float(item.get("score"))
                or self._as_float(item.get("similarity"))
                or self._as_float(item.get("relevance"))
            )
            if score is None or score >= float(min_score):
                filtered.append({**item, "_score": score})

        if not filtered:
            return [self._text_item(f"🔎 No results meeting the score threshold (≥ {min_score}).")]

        # Sort by score descending when present
        filtered.sort(key=lambda r: (
            r["_score"] is None, -(r["_score"] or 0.0)))

        output.append(self._text_item("🔎 Retrieval Results"))
        if min_score:
            output.append(self._text_item(f"Score threshold: ≥ {min_score}"))
        output.append(self._text_item(f"Results: {len(filtered)}"))

        for idx, item in enumerate(filtered, start=1):
            doc = item.get("document") or item.get("doc") or {}
            doc_id = self._get_doc_id(item) or self._get_doc_id(
                doc) or item.get("doc_id") or "unknown"
            kb_id = self._get_kb_id(item, self._get_kb_id(doc)) or "unknown"
            title = (
                item.get("title")
                or doc.get("title")
                or (doc.get("metadata") or {}).get("title")
                or "Untitled"
            )
            score = item.get("_score")
            score_str = f"{score:.3f}" if isinstance(score, float) else "n/a"

            snippet = (
                item.get("snippet")
                or item.get("text")
                or item.get("content")
                or doc.get("snippet")
                or doc.get("text")
                or doc.get("content")
                or ""
            )
            snippet = self._truncate(snippet, 300)

            header = f"- {idx}. {title} (score: {score_str})"
            meta = f"ID: {doc_id} | KB: {kb_id}"
            output.append(self._text_item(header))
            output.append(self._text_item(meta))
            if snippet:
                output.append(self._text_item(f"Snippet: {snippet}"))

        return output
