
from typing import Dict, List, Any


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
        formatted = []
        docs = response.get('documents', [])
        for doc in docs:
            doc_id = doc.get('id', 'unknown')
            title = doc.get('title', 'Untitled')
            created = doc.get('created_at', 'unknown date')
            formatted.append({
                'type': 'list_item',
                'content': f"📄 {title} (ID: {doc_id}) – Created: {created}"
            })
        return formatted

    def format_get_response(self, document_id: str, kb_id: str, content_data: Dict) -> List[Dict]:
        '''
        Format get document response.
        Args:
            document_id: ID of the requested document
            kb_id: Knowledge Base ID
            content_data: Raw content data of the document
        Returns:
            List of formatted content dictionaries for display
        '''
        title = content_data.get('title', 'Untitled')
        body = content_data.get('content', '')
        metadata = content_data.get('metadata', {})
        formatted = [
            {
                'type': 'header',
                'content': f"📄 Document: {title} (ID: {document_id})"
            },
            {
                'type': 'body',
                'content': body
            }
        ]
        if metadata:
            meta_str = ', '.join(f"{k}: {v}" for k, v in metadata.items())
            formatted.append({
                'type': 'metadata',
                'content': f"🔖 Metadata: {meta_str}"
            })
        return formatted

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
        return [
            {
                'type': 'success',
                'content': f"✅ Stored document '{title}' (ID: {doc_id}) in KB {kb_id}"
            }
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
        if status.lower() == 'success':
            emoji = '✅'
            msg = f"Document {doc_id} deleted from KB {kb_id}."
        else:
            emoji = '❌'
            msg = f"Failed to delete document {doc_id} from KB {kb_id}."
        return [
            {
                'type': 'status',
                'content': f"{emoji} {msg}"
            }
        ]

    def format_retrieve_response(self, response: Dict, min_score: float = 0.0) -> List[Dict]:
        '''
        Format retrieve documents response.
        Args:
            response: Raw API response from retrieve_documents
            min_score: Minimum score threshold to include a result
        Returns:
            List of formatted content dictionaries for display
        '''
        formatted = []
        results = response.get('results', [])
        for res in results:
            score = res.get('score', 0.0)
            if score < min_score:
                continue
            title = res.get('title', 'Untitled')
            doc_id = res.get('id', 'unknown')
            snippet = res.get('snippet', '')
            formatted.append({
                'type': 'result',
                'content': f"🔍 {title} (ID: {doc_id}) – Score: {score:.2f}\n{snippet}"
            })
        if not formatted:
            formatted.append({
                'type': 'info',
                'content': f"No results found with score ≥ {min_score}."
            })
        return formatted
