from typing import List, Dict


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
        docs = response.get("documents", [])
        if not docs:
            return [{
                "type": "text",
                "content": "📂 No documents found in the knowledge base."
            }]
        formatted = []
        for doc in docs:
            title = doc.get("title", "Untitled")
            doc_id = doc.get("id", "N/A")
            kb_id = doc.get("kb_id", "N/A")
            summary = doc.get("summary", "")
            content = f"📄 **{title}**\n- Document ID: `{doc_id}`\n- Knowledge Base ID: `{kb_id}`"
            if summary:
                content += f"\n- Summary: {summary}"
            formatted.append({
                "type": "text",
                "content": content
            })
        return formatted

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
        title = content_data.get("title", "Untitled")
        content = content_data.get("content", "")
        summary = content_data.get("summary", "")
        lines = [
            f"📄 **{title}**",
            f"- Document ID: `{document_id}`",
            f"- Knowledge Base ID: `{kb_id}`"
        ]
        if summary:
            lines.append(f"- Summary: {summary}")
        if content:
            lines.append("\n---\n")
            lines.append(content)
        return [{
            "type": "text",
            "content": "\n".join(lines)
        }]

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
        return [{
            "type": "text",
            "content": (
                f"✅ Document stored successfully!\n"
                f"- Title: **{title}**\n"
                f"- Document ID: `{doc_id}`\n"
                f"- Knowledge Base ID: `{kb_id}`"
            )
        }]

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
        if status.lower() == "success":
            emoji = "🗑️"
            msg = "Document deleted successfully."
        else:
            emoji = "⚠️"
            msg = f"Failed to delete document (status: {status})."
        return [{
            "type": "text",
            "content": (
                f"{emoji} {msg}\n"
                f"- Document ID: `{doc_id}`\n"
                f"- Knowledge Base ID: `{kb_id}`"
            )
        }]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve response.
        Args:
            response: Raw API response from retrieve
            min_score: Minimum relevance score threshold for filtering results
        Returns:
            List of formatted content dictionaries for display
        '''
        results = response.get("results", [])
        if not results:
            return [{
                "type": "text",
                "content": "🔍 No relevant documents found."
            }]
        formatted = []
        for i, res in enumerate(results, 1):
            score = res.get("score", 0.0)
            if score < min_score:
                continue
            doc_id = res.get("document_id", "N/A")
            kb_id = res.get("kb_id", "N/A")
            title = res.get("title", "Untitled")
            snippet = res.get("snippet", "")
            content = (
                f"🔎 **Result {i}**\n"
                f"- Title: **{title}**\n"
                f"- Document ID: `{doc_id}`\n"
                f"- Knowledge Base ID: `{kb_id}`\n"
                f"- Relevance Score: `{score:.3f}`"
            )
            if snippet:
                content += f"\n- Snippet: {snippet}"
            formatted.append({
                "type": "text",
                "content": content
            })
        if not formatted:
            return [{
                "type": "text",
                "content": "🔍 No relevant documents found above the score threshold."
            }]
        return formatted
