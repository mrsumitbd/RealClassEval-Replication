from typing import Dict, List, Any, Optional


class MemoryFormatter:
    '''
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    '''

    def _text(self, text: str) -> Dict[str, str]:
        return {"type": "text", "text": text}

    def _safe_get(self, obj: Dict, *keys: str, default: Any = None) -> Any:
        cur = obj
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur

    def _bool_success(self, status: Optional[str]) -> bool:
        if status is None:
            return False
        s = str(status).strip().lower()
        return s in {"ok", "success", "succeeded", "deleted", "completed", "true", "1"}

    def format_list_response(self, response: Dict) -> List[Dict]:
        '''
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        '''
        docs = (
            self._safe_get(response, "data")
            or self._safe_get(response, "documents")
            or self._safe_get(response, "results")
            or []
        )

        if not isinstance(docs, list):
            docs = []

        header = self._text(f"📚 Documents found: {len(docs)}")
        if not docs:
            return [header, self._text("No documents available.")]

        out: List[Dict] = [header]
        for i, d in enumerate(docs, start=1):
            doc_id = d.get("id") or d.get(
                "document_id") or d.get("doc_id") or "unknown"
            kb_id = (
                d.get("knowledge_base_id")
                or d.get("kb_id")
                or self._safe_get(d, "knowledge_base", "id")
                or "unknown"
            )
            title = d.get("title") or d.get(
                "name") or d.get("filename") or "(untitled)"
            created = d.get("created_at") or d.get(
                "created") or d.get("timestamp") or ""
            line = f"• {i}. 📝 {title}\n   - Doc ID: {doc_id}\n   - KB ID: {kb_id}"
            if created:
                line += f"\n   - Created: {created}"
            out.append(self._text(line))
        return out

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
        title = (
            (content_data or {}).get("title")
            or (content_data or {}).get("name")
            or "(untitled)"
        )
        header = self._text(f"📄 Retrieved document: {title}")
        meta = [
            self._text(f"• Doc ID: {document_id}"),
            self._text(f"• KB ID: {kb_id}"),
        ]

        blocks: List[Dict] = [header] + meta

        source = (content_data or {}).get(
            "source") or (content_data or {}).get("url")
        if source:
            blocks.append(self._text(f"• Source: {source}"))

        metadata = (content_data or {}).get("metadata")
        if isinstance(metadata, dict) and metadata:
            rendered = "; ".join(f"{k}: {v}" for k, v in metadata.items())
            blocks.append(self._text(f"• Metadata: {rendered}"))

        sections = (content_data or {}).get("sections")
        if isinstance(sections, list) and sections:
            blocks.append(self._text("🧩 Sections:"))
            for i, sec in enumerate(sections, start=1):
                s_title = (sec or {}).get("title") or (
                    sec or {}).get("heading") or f"Section {i}"
                s_body = (sec or {}).get("content") or (
                    sec or {}).get("text") or ""
                snippet = s_body.strip()
                if len(snippet) > 600:
                    snippet = snippet[:600].rstrip() + "…"
                blocks.append(self._text(f"  {i}. {s_title}\n     {snippet}"))
        else:
            content = (content_data or {}).get("content") or (
                content_data or {}).get("text") or ""
            if content:
                snippet = content.strip()
                if len(snippet) > 1000:
                    snippet = snippet[:1000].rstrip() + "…"
                blocks.append(self._text("🧾 Content:"))
                blocks.append(self._text(snippet))
            else:
                blocks.append(self._text("No content available."))

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
        return [
            self._text("✅ Document stored successfully"),
            self._text(f"• Title: {title_display}"),
            self._text(f"• Doc ID: {doc_id}"),
            self._text(f"• KB ID: {kb_id}"),
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
        ok = self._bool_success(status)
        icon = "✅" if ok else "❌"
        headline = "Document deleted" if ok else "Deletion failed"
        details = [
            self._text(f"• Status: {status}"),
            self._text(f"• Doc ID: {doc_id}"),
            self._text(f"• KB ID: {kb_id}"),
        ]
        return [self._text(f"{icon} {headline}")] + details

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve response.
        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results
        Returns:
            List of formatted content dictionaries for display
        '''
        # Try common containers
        items = (
            self._safe_get(response, "data")
            or self._safe_get(response, "results")
            or self._safe_get(response, "matches")
            or []
        )
        if not isinstance(items, list):
            items = []

        # Normalize entries
        normalized = []
        for it in items:
            if not isinstance(it, dict):
                continue
            score = (
                it.get("score")
                or it.get("similarity")
                or it.get("relevance")
                or self._safe_get(it, "metadata", "score")
                or 0.0
            )
            try:
                score_val = float(score)
            except Exception:
                score_val = 0.0

            doc = it.get("document") if isinstance(
                it.get("document"), dict) else {}
            # Fallback to top-level fields if no nested document
            doc_id = (
                doc.get("id")
                or it.get("document_id")
                or it.get("id")
                or self._safe_get(it, "metadata", "document_id")
                or "unknown"
            )
            kb_id = (
                doc.get("knowledge_base_id")
                or it.get("knowledge_base_id")
                or self._safe_get(it, "metadata", "knowledge_base_id")
                or "unknown"
            )
            title = (
                doc.get("title")
                or it.get("title")
                or self._safe_get(it, "metadata", "title")
                or "(untitled)"
            )
            content = (
                doc.get("content")
                or doc.get("text")
                or it.get("content")
                or it.get("text")
                or self._safe_get(it, "metadata", "snippet")
                or ""
            )
            snippet = content.strip()
            if len(snippet) > 400:
                snippet = snippet[:400].rstrip() + "…"

            normalized.append(
                {
                    "score": score_val,
                    "doc_id": doc_id,
                    "kb_id": kb_id,
                    "title": title,
                    "snippet": snippet,
                }
            )

        # Filter and sort
        results = [r for r in normalized if r["score"] >= float(min_score)]
        results.sort(key=lambda x: x["score"], reverse=True)

        header = self._text(
            f"🔎 Retrieval results: {len(results)} match(es) "
            + (f"(min score ≥ {min_score})" if min_score > 0 else "")
        )
        if not results:
            return [header, self._text("No matches found.")]

        out: List[Dict] = [header]
        for i, r in enumerate(results, start=1):
            pct = f"{r['score']*100:.1f}%"
            block_lines = [
                f"{i}. 📌 {r['title']}  •  Relevance: {pct}",
                f"   - Doc ID: {r['doc_id']}",
                f"   - KB ID: {r['kb_id']}",
            ]
            if r["snippet"]:
                block_lines.append(f"   - Snippet: {r['snippet']}")
            out.append(self._text("\n".join(block_lines)))

        return out
