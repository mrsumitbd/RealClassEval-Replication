
from typing import Dict, List


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
            doc_id = doc.get("id", "N/A")
            title = doc.get("title", "Untitled")
            created = doc.get("created_at", "Unknown date")
            formatted.append({
                "type": "text",
                "content": f"📄 **{title}**\nID: `{doc_id}`\nCreated: {created}"
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
        meta = content_data.get("metadata", {})
        meta_str = ""
        if meta:
            meta_str = "\n".join([f"- {k}: {v}" for k, v in meta.items()])
            meta_str = f"\n**Metadata:**\n{meta_str}"
        return [{
            "type": "text",
            "content": (
                f"📄 **{title}**\n"
                f"ID: `{document_id}`\n"
                f"Knowledge Base: `{kb_id}`\n"
                f"{meta_str}\n"
                f"---\n"
                f"{content}"
            )
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
                f"Title: **{title}**\n"
                f"ID: `{doc_id}`\n"
                f"Knowledge Base: `{kb_id}`"
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
                f"ID: `{doc_id}`\n"
                f"Knowledge Base: `{kb_id}`"
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
        filtered = [r for r in results if r.get("score", 0.0) >= min_score]
        if not filtered:
            return [{
                "type": "text",
                "content": "🔍 No relevant documents found."
            }]
        formatted = []
        for idx, r in enumerate(filtered, 1):
            doc_id = r.get("id", "N/A")
            title = r.get("title", "Untitled")
            score = r.get("score", 0.0)
            snippet = r.get("snippet", r.get("content", ""))
            kb_id = r.get("kb_id", "N/A")
            formatted.append({
                "type": "text",
                "content": (
                    f"🔎 **Result {idx}**\n"
                    f"Title: **{title}**\n"
                    f"ID: `{doc_id}`\n"
                    f"Knowledge Base: `{kb_id}`\n"
                    f"Relevance Score: {score:.2f}\n"
                    f"---\n"
                    f"{snippet}"
                )
            })
        return formatted
