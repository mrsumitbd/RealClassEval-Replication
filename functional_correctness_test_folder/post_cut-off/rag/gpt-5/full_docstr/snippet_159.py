from typing import Dict, List, Any, Optional


class MemoryFormatter:
    '''
    Formats memory tool responses for display.
    This class handles formatting the raw API responses into user-friendly
    output with proper structure, emoji indicators, and readable formatting.
    Each method corresponds to a specific action type's response format.
    '''

    def _truncate(self, text: str, limit: int = 800) -> str:
        if not isinstance(text, str):
            text = str(text)
        if len(text) <= limit:
            return text
        return text[: max(0, limit - 1)].rstrip() + '…'

    def _safe_list(self, response: Any) -> List[Dict]:
        if response is None:
            return []
        if isinstance(response, list):
            return response
        if isinstance(response, dict):
            for key in ('data', 'documents', 'items', 'results'):
                if key in response and isinstance(response[key], list):
                    return response[key]
            if 'id' in response:
                return [response]
        return []

    def _get(self, obj: Dict, *keys, default=None):
        for k in keys:
            if k in obj:
                return obj[k]
        return default

    def _bool_status(self, status: Any) -> bool:
        if isinstance(status, bool):
            return status
        if status is None:
            return False
        s = str(status).strip().lower()
        return s in {'ok', 'okay', 'success', 'succeeded', 'true', '1', 'completed', 'deleted', 'done'}

    def _format_metadata_lines(self, metadata: Any, max_items: int = 10) -> Optional[str]:
        if not metadata:
            return None
        if isinstance(metadata, dict):
            items = list(metadata.items())
        elif isinstance(metadata, list):
            items = [(str(i), v) for i, v in enumerate(metadata)]
        else:
            return None
        lines = []
        for i, (k, v) in enumerate(items[:max_items]):
            try:
                v_str = self._truncate(
                    v if isinstance(v, str) else str(v), 160)
            except Exception:
                v_str = str(v)
            lines.append(f"- {k}: {v_str}")
        if len(items) > max_items:
            lines.append(f"- … {len(items) - max_items} more")
        return "\n".join(lines)

    def format_list_response(self, response: Dict) -> List[Dict]:
        '''
        Format list documents response.
        Args:
            response: Raw API response from list_knowledge_base_documents
        Returns:
            List of formatted content dictionaries for display
        '''
        docs = self._safe_list(response)
        n = len(docs)
        contents: List[Dict] = []
        header = f"📚 Knowledge Base Documents: {n}"
        contents.append({"type": "text", "text": header})
        if n == 0:
            contents.append({"type": "text", "text": "No documents found."})
            return contents
        for d in docs:
            title = self._get(d, 'title', 'name',
                              'file_name', default='(untitled)')
            doc_id = self._get(d, 'id', 'doc_id', 'document_id', default='—')
            kb_id = self._get(d, 'kb_id', 'knowledge_base_id',
                              'knowledgeBaseId', default='—')
            source = self._get(d, 'source', 'origin', default=None)
            status = self._get(d, 'status', default=None)
            line = f"- {title}"
            meta_bits = []
            if source:
                meta_bits.append(f"source: {source}")
            if status:
                meta_bits.append(f"status: {status}")
            meta = f" ({', '.join(meta_bits)})" if meta_bits else ""
            line += f"{meta}\n  doc: {doc_id} | kb: {kb_id}"
            contents.append({"type": "text", "text": line})
        return contents

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
        contents: List[Dict] = []
        title = self._get(content_data or {}, 'title',
                          'name', default='(untitled)')
        contents.append({"type": "text", "text": "📄 Document Retrieved"})
        contents.append(
            {"type": "text", "text": f"Title: {title}\ndoc: {document_id}\nkb: {kb_id}"})
        summary = self._get(content_data, 'summary',
                            'description', default=None)
        if summary:
            contents.append(
                {"type": "text", "text": f"📝 Summary:\n{self._truncate(summary, 1200)}"})
        # Prefer main content/text
        text = self._get(content_data, 'text', 'content', 'body', default=None)
        if text:
            contents.append(
                {"type": "text", "text": f"🧾 Content:\n{self._truncate(text, 2000)}"})
        # If chunks/sections available
        chunks = self._get(content_data, 'chunks', 'sections', default=None)
        if isinstance(chunks, list) and not text:
            combined = []
            for c in chunks[:5]:
                piece = self._get(c if isinstance(c, dict)
                                  else {}, 'text', 'content', default=c)
                combined.append(str(piece))
            if combined:
                preview = "\n\n".join([self._truncate(p, 400)
                                      for p in combined])
                more = "" if len(
                    chunks) <= 5 else f"\n… {len(chunks) - 5} more section(s)"
                contents.append(
                    {"type": "text", "text": f"🧩 Sections (preview):\n{preview}{more}"})
        metadata = self._get(content_data, 'metadata', 'meta', default=None)
        meta_lines = self._format_metadata_lines(metadata)
        if meta_lines:
            contents.append(
                {"type": "text", "text": f"📎 Metadata:\n{meta_lines}"})
        return contents

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
        title_disp = title or '(untitled)'
        return [
            {"type": "text", "text": "✅ Document Stored"},
            {"type": "text", "text": f"Title: {title_disp}\ndoc: {doc_id}\nkb: {kb_id}"}
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
        ok = self._bool_status(status)
        emoji = "🗑️" if ok else "⚠️"
        headline = f"{emoji} Delete Document {'Succeeded' if ok else 'Failed'}"
        detail = f"doc: {doc_id}\nkb: {kb_id}\nstatus: {status}"
        return [
            {"type": "text", "text": headline},
            {"type": "text", "text": detail}
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
        items = self._safe_list(response)
        # Normalize fields
        normalized = []
        for it in items:
            if not isinstance(it, dict):
                it = {"text": str(it)}
            doc_id = self._get(it, 'document_id', 'doc_id', 'id', default='—')
            kb_id = self._get(it, 'kb_id', 'knowledge_base_id', default='—')
            score = self._get(it, 'score', 'similarity',
                              'relevance', default=None)
            try:
                score_f = float(score) if score is not None else None
            except Exception:
                score_f = None
            title = self._get(it, 'title', 'document_title', default=None)
            if not title:
                md = self._get(it, 'metadata', 'meta', default={})
                if isinstance(md, dict):
                    title = md.get('title') or md.get('name')
            text = self._get(it, 'text', 'content',
                             'chunk', 'snippet', default='')
            metadata = self._get(it, 'metadata', 'meta', default=None)
            normalized.append({
                "doc_id": doc_id,
                "kb_id": kb_id,
                "score": score_f,
                "raw_score": score,
                "title": title,
                "text": text,
                "metadata": metadata,
            })
        # Filter and sort
        if min_score is not None:
            filtered = [r for r in normalized if r["score"]
                        is None or r["score"] >= float(min_score)]
        else:
            filtered = normalized
        filtered.sort(key=lambda r: (
            r["score"] is not None, r["score"]), reverse=True)
        contents: List[Dict] = []
        if not filtered:
            contents.append(
                {"type": "text", "text": "🔎 No matching documents found."})
            return contents
        header = f"🔎 Retrieved Results: {len(filtered)}"
        if min_score:
            header += f" (min score {min_score})"
        contents.append({"type": "text", "text": header})
        for idx, r in enumerate(filtered, start=1):
            score_txt = f"{r['score']:.3f}" if isinstance(r['score'], float) else (
                "n/a" if r['score'] is None else str(r['score']))
            title = r["title"] or "(untitled)"
            snippet = self._truncate(r["text"] or "", 400)
            block_lines = [
                f"{idx}. {title}  •  score: {score_txt}",
            ]
            if snippet:
                block_lines.append(snippet)
            block_lines.append(f"doc: {r['doc_id']} | kb: {r['kb_id']}")
            meta_lines = self._format_metadata_lines(
                r["metadata"], max_items=5)
            if meta_lines:
                block_lines.append("meta:")
                block_lines.append(meta_lines)
            contents.append({"type": "text", "text": "\n".join(block_lines)})
        return contents
