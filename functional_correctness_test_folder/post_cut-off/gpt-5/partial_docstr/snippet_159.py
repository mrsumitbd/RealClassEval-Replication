from typing import Dict, List, Any, Optional


class MemoryFormatter:
    '''
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    '''

    def _text_block(self, text: str) -> Dict[str, Any]:
        return {"type": "text", "text": text}

    def _safe_str(self, value: Any, default: str = "—") -> str:
        if value is None:
            return default
        if isinstance(value, (dict, list)):
            return str(value)
        s = str(value).strip()
        return s if s else default

    def _fmt_kv(self, key: str, value: Any, default: str = "—") -> str:
        return f"{key}: {self._safe_str(value, default)}"

    def _coerce_score(self, value: Any) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(value)
        except Exception:
            return None

    def _first_nonempty(self, data: Dict, keys: List[str], default: Any = None) -> Any:
        for k in keys:
            if k in data and data[k] not in (None, "", [], {}):
                return data[k]
        return default

    def format_list_response(self, response: Dict) -> List[Dict]:
        '''
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        '''
        docs = []
        # Common possible locations for documents
        for key in ("data", "documents", "items", "results"):
            v = response.get(key)
            if isinstance(v, list):
                docs = v
                break

        if not docs:
            return [self._text_block("📚 No documents found.")]

        out: List[Dict] = []
        out.append(self._text_block(f"📚 Found {len(docs)} document(s):"))

        for i, d in enumerate(docs, start=1):
            # Try to normalize fields
            title = self._first_nonempty(
                d, ["title", "name", "document_title"], "(untitled)")
            doc_id = self._first_nonempty(
                d, ["id", "document_id", "doc_id"], "unknown")
            kb_id = self._first_nonempty(
                d, ["knowledge_base_id", "kb_id"], "unknown")
            source = self._first_nonempty(
                d, ["url", "source_url", "path", "source"], None)
            created = self._first_nonempty(
                d, ["created_at", "created", "inserted_at"], None)
            updated = self._first_nonempty(
                d, ["updated_at", "updated", "modified_at"], None)
            size = self._first_nonempty(
                d, ["size", "bytes", "content_size"], None)
            status = self._first_nonempty(d, ["status", "state"], None)

            lines = [
                f"📄 {i}. {self._safe_str(title)}",
                self._fmt_kv("ID", doc_id),
                self._fmt_kv("KB", kb_id),
            ]
            if source:
                lines.append(self._fmt_kv("Source", source))
            if created:
                lines.append(self._fmt_kv("Created", created))
            if updated:
                lines.append(self._fmt_kv("Updated", updated))
            if size:
                lines.append(self._fmt_kv("Size", size))
            if status:
                lines.append(self._fmt_kv("Status", status))

            out.append(self._text_block("\n".join(lines)))

        return out

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        title = self._first_nonempty(
            content_data, ["title", "name", "document_title"], "(untitled)")
        source = self._first_nonempty(
            content_data, ["url", "source_url", "path", "source"], None)
        status = self._first_nonempty(content_data, ["status", "state"], None)
        created = self._first_nonempty(
            content_data, ["created_at", "created", "inserted_at"], None)
        updated = self._first_nonempty(
            content_data, ["updated_at", "updated", "modified_at"], None)
        metadata = self._first_nonempty(
            content_data, ["metadata", "meta"], None)

        # Prefer snippet/preview over full content if present
        content = self._first_nonempty(
            content_data, ["snippet", "preview", "text_preview"], None)
        if content is None:
            content = self._first_nonempty(
                content_data, ["content", "text", "body"], None)

        # Trim very long content
        content_str = None
        if content is not None:
            s = self._safe_str(content)
            max_len = 1200
            if len(s) > max_len:
                s = s[:max_len].rstrip() + "…"
            content_str = s

        header = f"📄 Document details"
        lines = [
            header,
            self._fmt_kv("Title", title),
            self._fmt_kv("ID", document_id or self._first_nonempty(
                content_data, ["id", "document_id"], "unknown")),
            self._fmt_kv("KB", kb_id or self._first_nonempty(
                content_data, ["knowledge_base_id", "kb_id"], "unknown")),
        ]
        if source:
            lines.append(self._fmt_kv("Source", source))
        if status:
            lines.append(self._fmt_kv("Status", status))
        if created:
            lines.append(self._fmt_kv("Created", created))
        if updated:
            lines.append(self._fmt_kv("Updated", updated))
        if metadata:
            lines.append(self._fmt_kv("Metadata", metadata))

        out: List[Dict] = [self._text_block("\n".join(lines))]
        if content_str:
            out.append(self._text_block(f"🧾 Content\n{content_str}"))
        else:
            out.append(self._text_block("🧾 Content\n—"))

        return out

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
        lines = [
            "✅ Document stored",
            self._fmt_kv("Title", title or "(untitled)"),
            self._fmt_kv("ID", doc_id or "unknown"),
            self._fmt_kv("KB", kb_id or "unknown"),
        ]
        return [self._text_block("\n".join(lines))]

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
        ok = normalized in {"ok", "success",
                            "deleted", "done", "succeeded", "true"}
        emoji = "🗑️" if ok else "⚠️"
        title = "Document deleted" if ok else "Delete failed"

        lines = [
            f"{emoji} {title}",
            self._fmt_kv("ID", doc_id or "unknown"),
            self._fmt_kv("KB", kb_id or "unknown"),
            self._fmt_kv("Status", status or ("success" if ok else "failed")),
        ]
        return [self._text_block("\n".join(lines))]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        # Extract results list
        results = []
        for key in ("results", "data", "matches", "items"):
            v = response.get(key)
            if isinstance(v, list):
                results = v
                break

        if not results:
            return [self._text_block("🔎 No results found.")]

        # Normalize results into a common structure
        normalized = []
        for item in results:
            # Score
            score = self._coerce_score(
                self._first_nonempty(
                    item, ["score", "similarity", "relevance", "distance"], None)
            )
            # Document info might be nested
            doc = item.get("document") if isinstance(item, dict) else None
            if not isinstance(doc, dict):
                doc = {}

            # Flatten at top-level if fields are not nested
            title = self._first_nonempty(item, ["title", "name"], None)
            if title is None:
                title = self._first_nonempty(
                    doc, ["title", "name", "document_title"], "(untitled)")

            doc_id = self._first_nonempty(
                item, ["id", "document_id", "doc_id"], None)
            if doc_id is None:
                doc_id = self._first_nonempty(
                    doc, ["id", "document_id", "doc_id"], "unknown")

            kb_id = self._first_nonempty(
                item, ["knowledge_base_id", "kb_id"], None)
            if kb_id is None:
                kb_id = self._first_nonempty(
                    doc, ["knowledge_base_id", "kb_id"], "unknown")

            # Snippet/content
            snippet = self._first_nonempty(
                item, ["snippet", "preview", "text"], None)
            if snippet is None:
                snippet = self._first_nonempty(
                    doc, ["snippet", "preview", "text", "content", "body"], None)

            normalized.append(
                {
                    "score": score,
                    "title": title or "(untitled)",
                    "id": doc_id or "unknown",
                    "kb_id": kb_id or "unknown",
                    "snippet": snippet,
                }
            )

        # Filter by min_score
        filtered = []
        for r in normalized:
            s = r["score"]
            if s is None or s >= min_score:
                filtered.append(r)

        if not filtered:
            return [self._text_block("🔎 No results meet the score threshold.")]

        # Sort by score desc when available
        filtered.sort(key=lambda x: (
            x["score"] is not None, x["score"]), reverse=True)

        out: List[Dict] = []
        out.append(self._text_block(
            f"🔎 Retrieved {len(filtered)} result(s) (min score {min_score})."))

        for i, r in enumerate(filtered, start=1):
            score_str = "—"
            if r["score"] is not None:
                pct = max(0.0, min(1.0, r["score"])) * 100.0
                score_str = f"{pct:.1f}%"

            lines = [
                f"📌 {i}. {self._safe_str(r['title'])}",
                self._fmt_kv("Score", score_str),
                self._fmt_kv("ID", r["id"]),
                self._fmt_kv("KB", r["kb_id"]),
            ]

            if r.get("snippet"):
                snippet = self._safe_str(r["snippet"])
                max_len = 600
                if len(snippet) > max_len:
                    snippet = snippet[:max_len].rstrip() + "…"
                lines.append(f"Snippet: {snippet}")

            out.append(self._text_block("\n".join(lines)))

        return out
